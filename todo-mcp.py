# import libraries
from fastmcp import FastMCP
from typing import Annotated, NamedTuple

from todo_db import TodoDB

# Create the DB
todo_db = TodoDB(db_file="/opt/tmp/tasks.json")
#todo_db.sample_data()

# Todo Class
class Todo(NamedTuple):
   filename: Annotated[str, "Source file containing the #TODO"]
   text: Annotated[str, "#TODO text"]
   line_num: Annotated[int, "Line number of the #TODO line from the source file"]

# Create the MCP server
mcp = FastMCP('TODO-MCP')

# Tools
@mcp.tool(
   name = "tool_batch_add_todo",
   description="Add all #TODO from a source file"
)
def add_tods(todos: list[Todo]) -> int:
   for todo in todos:
      todo_db.add(todo[0], todo[1], todo[2])
   return len(todos)

@mcp.tool(
   name="tool_add_todo",
   description="Add a single #TODO text from a source file"
)
def add_todo(
      filename: Annotated[str, "Source file containing the #TODO"],
      text: Annotated[str, "#TODO text"],
      line_num: Annotated[int, "Line number of the #TODO line from the source file"]
):
   return todo_db.add(filename, text, line_num)

# Resource
@mcp.resource(
      name = "resource_get_todos_for_file",
      description="Get all todos from a file. Returns an empty array if source file does not exists or there are no #TODO from the file",
      uri="todo://{filename}/todos"
)
def get_todos_for_file(
      filename: Annotated[str, "Source file containing the #TODO"]
) -> list[str]:
   todos = todo_db.get(filename)
   return [ text for text in todos.values() ]

# Start the MCP
def main():
   mcp.run()

if __name__ == "__main__":
   main()