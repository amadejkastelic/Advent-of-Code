import enum
import math
import typing


class ModuleType(enum.Enum):
    BROADCAST = 'broadcaster'
    FLIP_FLOP = '%'
    CONJUNCTION = '&'


class Module(object):
    def __init__(self, name: str, destinations: typing.List[str]) -> None:
        self.destinations = destinations
        if name == ModuleType.BROADCAST.value:
            self.type = ModuleType.BROADCAST
            self.name = name
        else:
            self.type = ModuleType(name[0])
            self.name = name[1:]

        if self.type == ModuleType.FLIP_FLOP:
            self.state = False
        elif self.type == ModuleType.CONJUNCTION:
            self.inputs: typing.Dict[str, bool] = {}

    def set_con_inputs(self, inputs: typing.List[str]) -> None:
        for input in inputs:
            self.inputs[input] = False

    def add_con_input(self, input: str) -> None:
        self.inputs[input] = False

    def process_pulse(self, pulse: bool, input: str) -> typing.Optional[bool]:
        match self.type:
            case ModuleType.BROADCAST:
                return pulse
            case ModuleType.CONJUNCTION:
                self.inputs[input] = pulse
                return not all(self.inputs.values())
            case ModuleType.FLIP_FLOP:
                if pulse is True:
                    return None

                self.state = not self.state
                return self.state
            

def parse_input(path: str) -> typing.Dict[str, Module]:
    modules: typing.Dict[str, Module] = {}
    with open(path) as input_file:
        for line in input_file:
            name, dest = line.split(' -> ')
            module = Module(name=name, destinations=dest.strip().split(', '))
            modules[module.name] = module

    for con in list(filter(lambda module: module.type == ModuleType.CONJUNCTION, modules.values())):
        for module in modules.values():
            if con.name in module.destinations:
                con.add_con_input(module.name)

    return modules


if __name__ == '__main__':
    modules = parse_input('2023/day20/input.txt')

    lo, hi = 0, 0
    for _ in range(1000):
        queue = [(modules['broadcaster'], False, None)]
        while queue:
            module, pulse, inp = queue.pop(0)

            if pulse:
                hi += 1
            else:
                lo += 1

            if not module:
                continue
            pulse = module.process_pulse(pulse=pulse, input=inp)

            if pulse is not None:
                for dest in module.destinations:
                    queue.append((modules.get(dest), pulse, module.name))

    print(f'Part 1: {lo*hi}')

    modules = parse_input('2023/day20/input.txt')

    interesting_modules: typing.List[str] = []
    rx = Module(name='&rx', destinations=[])
    for module in modules.values():
        if 'rx' in module.destinations:
            rx.add_con_input(module.name)
            interesting_modules.append(module.name)
    modules['rx'] = rx

    presses: typing.Dict[str, int] = {}
    i = 0
    while True:
        i += 1
        queue = [(modules['broadcaster'], False, None)]
        while queue:
            module, pulse, inp = queue.pop(0)

            if module.name in interesting_modules and pulse:
                if inp in presses:
                    print(f'Part 2: {math.lcm(*presses.values())}')
                    exit(0)
                presses[inp] = i

            if pulse:
                hi += 1
            else:
                lo += 1

            if not module:
                continue

            pulse = module.process_pulse(pulse=pulse, input=inp)

            if pulse is not None:
                for dest in module.destinations:
                    queue.append((modules.get(dest), pulse, module.name))
