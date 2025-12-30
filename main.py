import json
from chatter import chat, component_registry
from chatter.components import basic_component

# has to start with discord


def main():
    with open("resources/socials.json") as file:
        socials = json.load(file)

    registry = component_registry.ComponentsRegistry()

    registry.add_component(basic_component.BaicComponent)
    registry.add_component(basic_component.social_component_factory(socials))

    chat.main()


if __name__ == "__main__":
    main()
