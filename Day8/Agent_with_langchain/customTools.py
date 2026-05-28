from langchain.tools import tool


@tool
def get_greet(name : str) -> str :
    ''' Generate a greeting message for the user '''
    return f" Hello {name} "

res = get_greet.invoke({"name":"nehal"})
print(res)