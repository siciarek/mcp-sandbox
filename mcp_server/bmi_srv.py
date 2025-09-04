from mcp.server.fastmcp import FastMCP

mcp = FastMCP("BMI")


# Tools
@mcp.tool()
def calculate_bmi(weight: int, height: int) -> str:
    """Calculate BMI"""
    with open('input.json', "w") as fp:
        import datetime
        fp.write(str([weight, height, str(datetime.datetime.now())]))
    return "BMI: " + str(weight / (height * height))


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
