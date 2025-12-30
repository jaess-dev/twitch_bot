import typing

from chatter.components.component_base import ComponentConstructor


class ComponentsRegistry(object):
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(ComponentsRegistry, cls).__new__(cls)
            cls.instance._components = []
            cls.instance._modules = []
        return cls.instance

    def add_component(self, component: ComponentConstructor):
        self._components.append(component)

    @property
    def components(self):
        return iter(self._components[:])

    def add_module(self, module: str) -> None:
        self._modules.append(module)

    @property
    def modules(self):
        return iter(self._modules[:])

    def __iter__(self) -> typing.Iterator[ComponentConstructor]:
        return iter(self._components[:])
