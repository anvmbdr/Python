#1
i = 1
while i < 6:
    print(i)
    if i == 3:
        break
    i += 1

#2
i = 1
while i < 10:       
    print(i)         
    if i == 5:      
        break        
    i += 1          

#3
i = 1
while i <= 10:        
    print("Number:", i) 
    if i == 4:           
        print("Stop")    
        break            
    i += 1

#4
i = 1
while i < 5:          # пока i < 5
    print(i)           # выводим i
    if i == 3:         # если i = 3
        break          # прерываем цикл
    i += 1
else:                  # выполняется, если break не сработал
    print("No break")

#5
i = 10
while i > 0:        # пока i > 0
    print(i)
    if i == 7:       # остановка на 7
        break
    i -= 1           # уменьшаем i

