# MCP Sample App

The following is and istruction how to setup and run the app.


# Set up

```bash
make setup
cp .env.dist .env
```

update variables in `.env` file.

# Run server

In the terminal run:

```bash
make bmi_srv
```

# Run client

In the second terminal run:

```bash
make client
```

Ask question about the math like `2 * 30` or BMI `My height is 190 and weight 103 what is my BMI`.
