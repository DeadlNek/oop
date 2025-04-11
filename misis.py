from abc import ABC, abstractmethod
from typing import List
from io import StringIO

# Базовый абстрактный класс для объектов, которые можно распечатать
class Printable(ABC):
    @abstractmethod
    def print_me(self, os, prefix="", is_last=False):
        pass

    @abstractmethod
    def clone(self):
        pass

    # Метод для преобразования объекта в строку
    def __str__(self):
        buf = StringIO()
        self.print_me(buf, is_last=True)
        return buf.getvalue().strip()

# Базовый класс для коллекций элементов
class BasicCollection(Printable):
    def __init__(self):
        self.items = []

    # Метод для добавления элемента в коллекцию
    def add(self, elem):
        self.items.append(elem)
        return self

    # Метод для поиска элемента в коллекции
    def find(self, elem):
        for item in self.items:
            if item == elem:
                return item
        return None

    # Метод для клонирования коллекции
    def clone(self):
        new_collection = self.__class__()
        new_collection.items = [item.clone() for item in self.items]
        return new_collection

    # Метод для печати всех элементов коллекции
    def print_me(self, os, prefix="", is_last=False):
        for i, item in enumerate(self.items):
            item.print_me(os, prefix, i == len(self.items) - 1)

# Базовый класс для компонентов компьютера
class Component(Printable, ABC):
    def __init__(self, numeric_val=0):
        self.numeric_val = numeric_val

# Класс для представления сетевого адреса
class Address(Printable):
    def __init__(self, addr):
        self.address = addr

    # Метод для печати адреса
    def print_me(self, os, prefix="", is_last=False):
        connector = "\\-" if is_last else "+-"
        os.write(f"{prefix}{connector}{self.address}\n")

    # Метод для клонирования адреса
    def clone(self):
        return Address(self.address)

# Класс для представления раздела на диске
class Partition(Printable):
    def __init__(self, size, name):
        self.size = size
        self.name = name

    # Метод для печати информации о разделе
    def print_me(self, os, prefix="", is_last=False):
        connector = "\\-" if is_last else "+-"
        os.write(f"{prefix}{connector}[{self.name}]: {self.size} GiB\n")

    # Метод для клонирования раздела
    def clone(self):
        return Partition(self.size, self.name)

# Класс компонента-диска с разделами
class Disk(Component):
    SSD = 0
    MAGNETIC = 1

    def __init__(self, storage_type, size):
        # Инициализация диска
        super().__init__(size)
        self.storage_type = storage_type
        self.partitions = []

    # Метод для добавления раздела на диск
    def add_partition(self, size, name):
        self.partitions.append((size, name))
        return self

    # Метод для печати информации о диске и его разделах
    def print_me(self, os, prefix="", is_last=False):
        type_str = "SSD" if self.storage_type == Disk.SSD else "HDD"
        connector = "\\-" if is_last else "+-"
        os.write(f"{prefix}{connector}{type_str}, {self.numeric_val} GiB\n")
        for i, (size, name) in enumerate(self.partitions):
            last = i == len(self.partitions) - 1
            new_prefix = prefix + ("  " if is_last else "| ")
            sub_connector = "\\-" if last else "+-"
            os.write(f"{new_prefix}{sub_connector}[{i}]: {size} GiB, {name}\n")

    # Метод для клонирования диска
    def clone(self):
        new_disk = Disk(self.storage_type, self.numeric_val)
        for part in self.partitions:
            new_disk.add_partition(*part)
        return new_disk

# Класс компонента CPU
class CPU(Component):
    def __init__(self, cores, mhz):
        # Инициализация CPU
        super().__init__(mhz)
        self.cores = cores

    # Метод для печати информации о CPU
    def print_me(self, os, prefix="", is_last=False):
        connector = "\\-" if is_last else "+-"
        os.write(f"{prefix}{connector}CPU, {self.cores} cores @ {self.numeric_val}MHz\n")

    # Метод для клонирования CPU
    def clone(self):
        return CPU(self.cores, self.numeric_val)

# Класс компонента памяти
class Memory(Component):
    def __init__(self, size):
        # Инициализация памяти
        super().__init__(size)

    # Метод для печати информации о памяти
    def print_me(self, os, prefix="", is_last=False):
        connector = "\\-" if is_last else "+-"
        os.write(f"{prefix}{connector}Memory, {self.numeric_val} MiB\n")

    # Метод для клонирования памяти
    def clone(self):
        return Memory(self.numeric_val)

# Класс компьютера с адресами и компонентами
class Computer(Printable):
    def __init__(self, name):
        self.name = name
        self.addresses: List[Address] = []
        self.components: List[Component] = []

    # Метод для добавления адреса к компьютеру
    def add_address(self, addr):
        if isinstance(addr, str):
            addr = Address(addr)
        self.addresses.append(addr)
        return self

    # Метод для добавления компонента к компьютеру
    def add_component(self, comp):
        self.components.append(comp)
        return self

    # Метод для печати информации о компьютере
    def print_me(self, os, prefix="", is_last=False):
        connector = "\\-" if is_last else "+-"
        os.write(f"{prefix}{connector}Host: {self.name}\n")
        new_prefix = prefix + ("  " if is_last else "| ")
        items = self.addresses + self.components
        for i, item in enumerate(items):
            item.print_me(os, new_prefix, i == len(items) - 1)

    # Метод для клонирования компьютера
    def clone(self):
        new_comp = Computer(self.name)
        new_comp.addresses = [addr.clone() for addr in self.addresses]
        new_comp.components = [comp.clone() for comp in self.components]
        return new_comp

# Класс сети с компьютерами
class Network(Printable):
    def __init__(self, name):
        self.name = name
        self.computers: List[Computer] = []

    # Метод для добавления компьютера в сеть
    def add_computer(self, comp):
        self.computers.append(comp)
        return self

    # Метод для поиска компьютера в сети по имени
    def find_computer(self, name):
        for comp in self.computers:
            if comp.name == name:
                return comp
        return None

    # Метод для печати всей сети
    def print_me(self, os, prefix="", is_last=False):
        os.write(f"Network: {self.name}\n")
        for i, comp in enumerate(self.computers):
            comp.print_me(os, "", i == len(self.computers) - 1)

    # Метод для клонирования сети
    def clone(self):
        new_net = Network(self.name)
        new_net.computers = [comp.clone() for comp in self.computers]
        return new_net

# Пример использования
def main():
    n = Network("MISIS network")
    
    # Добавление первого компьютера с компонентами
    n.add_computer(
        Computer("server1.misis.ru")
        .add_address("192.168.1.1")
        .add_component(CPU(4, 2500))
        .add_component(Memory(16000))
    )
    
    # Добавление второго компьютера с компонентами
    n.add_computer(
        Computer("server2.misis.ru")
        .add_address("10.0.0.1")
        .add_component(CPU(8, 3200))
        .add_component(
            Disk(Disk.MAGNETIC, 2000)
            .add_partition(500, "system")
            .add_partition(1500, "data")
        )
    )
    
    # Вывод всей сети
    print("=== Сеть ===")
    print(n)

if __name__ == "__main__":
    main()
