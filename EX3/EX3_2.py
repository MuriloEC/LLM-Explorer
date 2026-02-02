import operator
from dataclasses import dataclass
from typing import Annotated, Literal

from langgraph.graph import END, START, StateGraph



@dataclass
class State:
    nodes_path: Annotated[list[str], operator.add] 
    
    current_number: float = 0


def node_a(state: State) -> State:
    final_state: State = State(nodes_path=["A"], current_number=state.current_number)
    print("> node_a em execução", f"{state=}", f"{final_state=}")
    return final_state  


def node_b(state: State) -> State:
    final_state: State = State(nodes_path=["B"], current_number=state.current_number)
    print("> node_b em execução", f"{state=}", f"{final_state=}")
    return final_state  



def node_c(state: State) -> State:
    final_state: State = State(nodes_path=["C"], current_number=state.current_number)
    print("> node_c em execução", f"{state=}", f"{final_state=}")
    return final_state 



def the_conditions(state: State) -> Literal["goes_to_b", "goes_to_c"]:
    
    b_max_number = 50  

    if state.current_number <= b_max_number:
        
        return "goes_to_b"

    
    return "goes_to_c"




builder = StateGraph(
    State, input_schema=State, context_schema=None, output_schema=State
)

builder.add_node("A", node_a)
builder.add_node("B", node_b)
builder.add_node("C", node_c)  


builder.add_edge(START, "A")

builder.add_conditional_edges(
    "A",
    the_conditions,
    {
        "goes_to_b": "B",
        "goes_to_c": "C",
    },
)


builder.add_edge("B", END)
builder.add_edge("C", END)


graph = builder.compile()
print()

response = graph.invoke(State(nodes_path=[], current_number=10))
print(f"{response=}")
print()

response = graph.invoke(State(nodes_path=[], current_number=51))
print(f"{response=}")
print()