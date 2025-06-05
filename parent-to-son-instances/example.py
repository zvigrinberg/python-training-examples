from pydantic import BaseModel


class Parent(BaseModel):
    name: str
    description: str


class Child(Parent):
    misc: str

    def to_parent(self) -> Parent:
        return Parent(name=self.name, description=self.description)

    def to_parent_pydantic(self) -> Parent:
        return Parent(**self.model_dump(exclude={"misc"}))


if __name__ == "__main__":
    child = Child(name="child", description="This is Child", misc="blabla")
    # parent = Parent(name="parent", description="description")
    attrs = vars(child)
    print("child:")
    print(', '.join("%s: %s" % item for item in attrs.items()))
    attrs2 = vars(child.to_parent())
    print("to parent manual:")
    print(', '.join("%s: %s" % item for item in attrs2.items()))
    print("to parent pydantic:")
    attrs3 = vars(child.to_parent_pydantic())
    print(', '.join("%s: %s" % item for item in attrs3.items()))
