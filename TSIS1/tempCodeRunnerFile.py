import csv
import json
import os
import sys
from datetime import date, datetime
from typing import Optional

import psycopg2
import psycopg2.extras

from connect import get_connection


def _conn():
    conn = get_connection()
    conn.autocommit = False
    return conn


def _fmt_date(d) -> str:
    if d is None:
        return "-"
    if isinstance(d, (date, datetime)):
        return d.strftime("%Y-%m-%d")
    return str(d)


def _print_contacts(rows):
    if not rows:
        print("No results found.")
        return
    print("-" * 90)
    print(f"  {'ID':<5} {'Name':<22} {'Email':<28} {'Birthday':<12} {'Group':<10} Phones")
    print("-" * 90)
    for r in rows:
        phones = r.get("phones_list") or r.get("phones") or "-"
        print(
            f"  {str(r.get('id','')):<5} "
            f"{str(r.get('username','')):<22} "
            f"{str(r.get('email') or '-'):<28} "
            f"{_fmt_date(r.get('birthday')):<12} "
            f"{str(r.get('group_name') or '-'):<10} "
            f"{phones}"
        )
    print("-" * 90)


def _get_groups(cur) -> dict:
    cur.execute("SELECT id, name FROM groups ORDER BY name")
    return {row["name"]: row["id"] for row in cur.fetchall()}


def _resolve_or_create_group(cur, group_name: str) -> Optional[int]:
    if not group_name:
        return None
    cur.execute(
        "INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
        (group_name,)
    )
    cur.execute("SELECT id FROM groups WHERE name ILIKE %s", (group_name,))
    row = cur.fetchone()
    return row["id"] if row else None


def init_schema():
    base = os.path.dirname(__file__)
    for fname in ("schema.sql", "procedures.sql"):
        path = os.path.join(base, fname)
        if not os.path.exists(path):
            print(f"File {fname} not found.")
            continue
        with open(path, "r") as f:
            sql = f.read()
        try:
            conn = _conn()
            with conn.cursor() as cur:
                cur.execute(sql)
            conn.commit()
            conn.close()
            print(f"{fname} applied.")
        except Exception as e:
            print(f"Error in {fname}: {e}")


def filter_by_group():
    conn = _conn()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        groups = _get_groups(cur)
    conn.close()

    if not groups:
        print("No groups found.")
        return

    print("\nAvailable groups:")
    for i, name in enumerate(groups, 1):
        print(f"  {i}. {name}")
    choice = input("Group name (or number): ").strip()

    if choice.isdigit():
        names = list(groups.keys())
        idx = int(choice) - 1
        if 0 <= idx < len(names):
            choice = names[idx]

    conn = _conn()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(
            "SELECT c.id, c.username, c.email, c.birthday,"
            " g.name AS group_name,"
            " STRING_AGG(p.phone || ' (' || COALESCE(p.type,'?') || ')', ', '"
            "            ORDER BY p.id) AS phones_list"
            " FROM contacts c"
            " LEFT JOIN groups g ON g.id = c.group_id"
            " LEFT JOIN phones p ON p.contact_id = c.id"
            " WHERE g.name ILIKE %s"
            " GROUP BY c.id, c.username, c.email, c.birthday, g.name"
            " ORDER BY c.username",
            (choice,)
        )
        rows = cur.fetchall()
    conn.close()
    print(f"\nContacts in group '{choice}':")
    _print_contacts(rows)


def search_by_email():
    query = input("Email fragment: ").strip()
    if not query:
        return
    conn = _conn()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(
            "SELECT c.id, c.username, c.email, c.birthday,"
            " g.name AS group_name,"
            " STRING_AGG(p.phone || ' (' || COALESCE(p.type,'?') || ')', ', '"
            "            ORDER BY p.id) AS phones_list"
            " FROM contacts c"
            " LEFT JOIN groups g ON g.id = c.group_id"
            " LEFT JOIN phones p ON p.contact_id = c.id"
            " WHERE c.email ILIKE %s"
            " GROUP BY c.id, c.username, c.email, c.birthday, g.name"
            " ORDER BY c.username",
            (f"%{query}%",)
        )
        rows = cur.fetchall()
    conn.close()
    print(f"\nResults for '{query}':")
    _print_contacts(rows)


def sorted_contacts():
    print("\nSort by:  1) name   2) birthday   3) date added")
    choice = input("Choice [1/2/3]: ").strip()
    order_map = {"1": "c.username", "2": "c.birthday", "3": "c.id"}
    order_col = order_map.get(choice, "c.username")

    conn = _conn()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(
            f"SELECT c.id, c.username, c.email, c.birthday,"
            f" g.name AS group_name,"
            f" STRING_AGG(p.phone || ' (' || COALESCE(p.type,'?') || ')', ', '"
            f"            ORDER BY p.id) AS phones_list"
            f" FROM contacts c"
            f" LEFT JOIN groups g ON g.id = c.group_id"
            f" LEFT JOIN phones p ON p.contact_id = c.id"
            f" GROUP BY c.id, c.username, c.email, c.birthday, g.name"
            f" ORDER BY {order_col} NULLS LAST"
        )
        rows = cur.fetchall()
    conn.close()
    _print_contacts(rows)


def paginated_browse():
    page_size = 5
    page = 0

    def _fetch(offset):
        conn = _conn()
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                "SELECT c.id, c.username, c.email, c.birthday,"
                " g.name AS group_name,"
                " STRING_AGG(p.phone || ' (' || COALESCE(p.type,'?') || ')', ', '"
                "            ORDER BY p.id) AS phones_list"
                " FROM contacts c"
                " LEFT JOIN groups g ON g.id = c.group_id"
                " LEFT JOIN phones p ON p.contact_id = c.id"
                " GROUP BY c.id, c.username, c.email, c.birthday, g.name"
                " ORDER BY c.username"
                " LIMIT %s OFFSET %s",
                (page_size, offset)
            )
            rows = cur.fetchall()
        conn.close()
        return rows

    while True:
        rows = _fetch(page * page_size)
        print(f"\nPage {page + 1}")
        _print_contacts(rows)
        print("next (n) | prev (p) | quit (q)")
        cmd = input("> ").strip().lower()
        if cmd in ("n", "next"):
            if rows:
                page += 1
            else:
                print("Already at last page.")
        elif cmd in ("p", "prev"):
            if page > 0:
                page -= 1
            else:
                print("Already at first page.")
        elif cmd in ("q", "quit"):
            break


def export_to_json(filepath: str = "contacts_export.json"):
    conn = _conn()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(
            "SELECT c.id, c.username, c.email,"
            " c.birthday::text AS birthday,"
            " g.name AS group_name"
            " FROM contacts c"
            " LEFT JOIN groups g ON g.id = c.group_id"
            " ORDER BY c.username"
        )
        contacts = [dict(r) for r in cur.fetchall()]

        for c in contacts:
            cur.execute(
                "SELECT phone, type FROM phones WHERE contact_id = %s ORDER BY id",
                (c["id"],)
            )
            c["phones"] = [dict(p) for p in cur.fetchall()]
            del c["id"]

    conn.close()
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=2, ensure_ascii=False)
    print(f"{len(contacts)} contacts exported to '{filepath}'.")


def import_from_json(filepath: str = "contacts_export.json"):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            records = json.load(f)
    except FileNotFoundError:
        print(f"File '{filepath}' not found.")
        return
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        return

    conn = _conn()
    inserted = skipped = overwritten = 0

    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        for rec in records:
            name = rec.get("username", "").strip()
            if not name:
                continue

            group_id = _resolve_or_create_group(cur, rec.get("group_name"))

            cur.execute("SELECT id FROM contacts WHERE username = %s", (name,))
            existing = cur.fetchone()

            if existing:
                print(f"\nDuplicate: '{name}' already exists.")
                action = input("[s]kip / [o]verwrite? ").strip().lower()
                if action != "o":
                    skipped += 1
                    continue
                cur.execute(
                    "UPDATE contacts SET email = %s, birthday = %s, group_id = %s WHERE id = %s",
                    (rec.get("email"), rec.get("birthday"), group_id, existing["id"])
                )
                cur.execute("DELETE FROM phones WHERE contact_id = %s", (existing["id"],))
                contact_id = existing["id"]
                overwritten += 1
            else:
                cur.execute(
                    "INSERT INTO contacts (username, email, birthday, group_id)"
                    " VALUES (%s, %s, %s, %s) RETURNING id",
                    (name, rec.get("email"), rec.get("birthday"), group_id)
                )
                contact_id = cur.fetchone()["id"]
                inserted += 1

            for ph in rec.get("phones", []):
                cur.execute(
                    "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                    (contact_id, ph.get("phone"), ph.get("type", "mobile"))
                )

    conn.commit()
    conn.close()
    print(f"Import done - inserted: {inserted}, overwritten: {overwritten}, skipped: {skipped}.")


def import_from_csv(filepath: str = "contacts.csv"):
    try:
        f = open(filepath, newline="", encoding="utf-8")
    except FileNotFoundError:
        print(f"File '{filepath}' not found.")
        return

    reader = csv.DictReader(f)
    conn = _conn()
    inserted = 0

    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        for row in reader:
            name = row.get("username", "").strip()
            if not name:
                continue

            group_id = _resolve_or_create_group(cur, row.get("group", "").strip())
            email    = row.get("email", "").strip() or None
            birthday = row.get("birthday", "").strip() or None
            phone    = row.get("phone", "").strip()
            ph_type  = row.get("phone_type", "mobile").strip() or "mobile"

            cur.execute("SELECT id FROM contacts WHERE username = %s", (name,))
            existing = cur.fetchone()
            if existing:
                contact_id = existing["id"]
                cur.execute(
                    "UPDATE contacts"
                    " SET email = COALESCE(%s, email),"
                    "     birthday = COALESCE(%s::date, birthday),"
                    "     group_id = COALESCE(%s, group_id)"
                    " WHERE id = %s",
                    (email, birthday, group_id, contact_id)
                )
            else:
                cur.execute(
                    "INSERT INTO contacts (username, email, birthday, group_id)"
                    " VALUES (%s, %s, %s, %s) RETURNING id",
                    (name, email, birthday, group_id)
                )
                contact_id = cur.fetchone()["id"]
                inserted += 1

            if phone:
                cur.execute(
                    "SELECT 1 FROM phones WHERE contact_id=%s AND phone=%s",
                    (contact_id, phone)
                )
                if not cur.fetchone():
                    cur.execute(
                        "INSERT INTO phones (contact_id, phone, type) VALUES (%s,%s,%s)",
                        (contact_id, phone, ph_type)
                    )

    conn.commit()
    conn.close()
    f.close()
    print(f"CSV import done - {inserted} new contacts from '{filepath}'.")


def call_add_phone():
    name   = input("Contact name: ").strip()
    phone  = input("Phone number: ").strip()
    p_type = input("Type [home/work/mobile] (default: mobile): ").strip() or "mobile"
    conn = _conn()
    try:
        with conn.cursor() as cur:
            cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, p_type))
        conn.commit()
        print("Phone added.")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        conn.close()


def call_move_to_group():
    name  = input("Contact name: ").strip()
    group = input("Target group name: ").strip()
    conn = _conn()
    try:
        with conn.cursor() as cur:
            cur.execute("CALL move_to_group(%s, %s)", (name, group))
        conn.commit()
        print("Contact moved.")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        conn.close()


def call_search_contacts():
    query = input("Search (name / email / phone): ").strip()
    if not query:
        return
    conn = _conn()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("SELECT * FROM search_contacts(%s)", (query,))
        rows = cur.fetchall()
    conn.close()
    print(f"\nResults for '{query}':")
    _print_contacts(rows)


ACTIONS = {
    "1":  filter_by_group,
    "2":  search_by_email,
    "3":  sorted_contacts,
    "4":  paginated_browse,
    "5":  call_search_contacts,
    "6":  call_add_phone,
    "7":  call_move_to_group,
    "8":  lambda: export_to_json(input("Output file [contacts_export.json]: ").strip() or "contacts_export.json"),
    "9":  lambda: import_from_json(input("JSON file [contacts_export.json]: ").strip() or "contacts_export.json"),
    "10": lambda: import_from_csv(input("CSV file [contacts.csv]: ").strip() or "contacts.csv"),
    "11": init_schema,
}


def main():
    while True:
        print("\nPhoneBook - TSIS 1")
        print("1. Filter by group")
        print("2. Search by email")
        print("3. Show all contacts (sorted)")
        print("4. Paginated browse")
        print("5. Full search (name / email / phone)")
        print("6. Add phone to contact")
        print("7. Move contact to group")
        print("8. Export to JSON")
        print("9. Import from JSON")
        print("10. Import from CSV")
        print("11. Init DB schema")
        print("0. Exit")

        choice = input("Select: ").strip()
        if choice == "0":
            sys.exit(0)
        action = ACTIONS.get(choice)
        if action:
            try:
                action()
            except KeyboardInterrupt:
                print("\n(cancelled)")
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
