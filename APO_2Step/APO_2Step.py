from thespian.actors import *


class SimplestActor(Actor):
    """
    Объявляем класс - Простой актор, который в будущем станет агентом
    """
    def __init__(self):
        super().__init__()
        print('Создан новый актор')
        self.messages = []
        self.child_addresses = []
		
    def receiveMessage(self, msg, sender):
        print(f'Актор с адресом {self.myAddress} получил {msg} от {sender}')
        self.messages.append(msg)
        for message in self.messages:
            print(f'Актор с адресом {self.myAddress} ранее получал сообщение {message}')
        for child in self.child_addresses:
            print(f'Ретранслируем сообщение дочернему актору с адресом {child}')
            self.send(child, msg)
        if msg == 'CREATE_ACTOR':
            child_actor_address = self.createActor(SimplestActor)
            print(f'Создали нового актора, его адрес - {child_actor_address}')
            self.child_addresses.append(child_actor_address)


class NumberActor(Actor):
    def __init__(self):
        super().__init__()
        # В это поле будем сохранять полученное значение.
        self.value = 0
        
    def receiveMessage(self, msg, sender):
        print(f'Актор числа с адресом {self.myAddress} получил {msg} от {sender}')
        # Ожидаем, что в сообщении будет содержаться словарь со значением числа и адресом актора-калькулятора.
        self.value = msg.get('init_value')
        calculator_address = msg.get('calculator_address')
        # Отправляем калькулятору свое значение.
        self.send(calculator_address, self.value)

class OperationActor(Actor):
    def __init__(self):
        super().__init__()
        # В это поле будем сохранять полученное значение.
        self.operation = ''
        
    def receiveMessage(self, msg, sender):
        print(f'Актор операции с адресом {self.myAddress} получил {msg} от {sender}')
        # Ожидаем, что в сообщении будет содержаться словарь со значением математической операции и адресом актора-калькулятора.
        self.operation = msg['operation']
        calculator_address = msg.get('calculator_address')
        # Отправляем калькулятору свое значение.
        self.send(calculator_address, self.operation)


class CalculatorActor(Actor):
    def __init__(self):
        super().__init__()
        # Все полученные числа будем сохранять в списке.
        self.values = []
        
    def receiveMessage(self, msg, sender):
        print(f'Калькулятор {self.myAddress} получил: {msg}')
        
        if isinstance(msg, (int, float)):
            self.values.append(msg)
            print(f'Добавлено число: {msg}. Всего чисел: {len(self.values)}')
        
        elif isinstance(msg, str):
            if msg == 'sum':
                result = sum(self.values)
                print(f'Сумма: {result}')
            elif msg == 'multiply':
                result = 1
                for n in self.values: result *= n
                print(f'Произведение: {result}')
            elif msg == 'avg':
                avg = sum(self.values)/len(self.values) if self.values else 0
                print(f'Среднее значение: {avg}')
            elif msg == 'clear':
                self.values = []
                print('Список очищен')
            elif  msg == 'get values':
                print(f'Список чисел: {self.values}')
            else:
                print(f'Неизвестная операция: {msg}')

		
		
if __name__ == "__main__":
    # Создаем систему акторов, внутри которой они будут жить
    actorSystem = ActorSystem()
    # Создаем экземпляр созданного нами класса и сохраняем его адрес
    actorAddress1 = actorSystem.createActor(SimplestActor)
    # Отправляем по сохраненному адресу сообщение.
    actorSystem.tell(actorAddress1, "Первое сообщение")
    actorSystem.tell(actorAddress1, 'CREATE_ACTOR')
    actorSystem.tell(actorAddress1, 'RETRANSLATED MESSAGE')
	
    print('________________________________')
    print('Запускаем работу системы с калькулятором')
    
    # Создаем актор-калькулятор, сохраняем его адрес.
    calculator_address = actorSystem.createActor(CalculatorActor)
    
    # Создаем актор-число
    number_agent_1 = actorSystem.createActor(NumberActor)
    # Формируем сообщение со значением числа и адресом калькулятора.
    init_message_1 = {'init_value': 1, 'calculator_address': calculator_address}
    
    # Отправляем актору числа сообщение, после которого он должен отправить другое сообщение калькулятору.
    actorSystem.tell(number_agent_1, init_message_1)
    
    number_agent_2 = actorSystem.createActor(NumberActor)
    init_message_2 = {'init_value': 2, 'calculator_address': calculator_address}
    actorSystem.tell(number_agent_2, init_message_2)
    
    number_agent_3 = actorSystem.createActor(NumberActor)
    init_message_3 = {'init_value': 3, 'calculator_address': calculator_address}
    actorSystem.tell(number_agent_3, init_message_3)

    operation_agent_1 = actorSystem.createActor(OperationActor)
    operation_message_1 = {'operation': 'sum', 'calculator_address': calculator_address}
    actorSystem.tell(operation_agent_1, operation_message_1)

    operation_agent_2 = actorSystem.createActor(OperationActor)
    operation_message_2 = {'operation': 'avg', 'calculator_address': calculator_address}
    actorSystem.tell(operation_agent_2, operation_message_2)

    operation_agent_3 = actorSystem.createActor(OperationActor)
    operation_message_3 = {'operation': 'multiply', 'calculator_address': calculator_address}
    actorSystem.tell(operation_agent_3, operation_message_3)

    operation_agent_4 = actorSystem.createActor(OperationActor)
    operation_message_4 = {'operation': 'some_operation', 'calculator_address': calculator_address}
    actorSystem.tell(operation_agent_4, operation_message_4)

    operation_agent_5 = actorSystem.createActor(OperationActor)
    operation_message_5 = {'operation': 'get values', 'calculator_address': calculator_address}
    actorSystem.tell(operation_agent_5, operation_message_5)

    operation_agent_6 = actorSystem.createActor(OperationActor)
    operation_message_6 = {'operation': 'clear', 'calculator_address': calculator_address}
    actorSystem.tell(operation_agent_6, operation_message_6)


