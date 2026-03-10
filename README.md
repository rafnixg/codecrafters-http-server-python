[![progress-banner](https://backend.codecrafters.io/progress/http-server/3521227d-25a0-4bb5-89d3-3886f19ff1b1)](https://app.codecrafters.io/users/codecrafters-bot?r=2qF)

# 🌐 Build Your Own HTTP Server — Python

A fully functional **HTTP/1.1 server** built in Python as part of the
[CodeCrafters "Build Your Own HTTP server" Challenge](https://app.codecrafters.io/courses/http-server/overview).

[HTTP](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol) is the
protocol that powers the web. This project implements an HTTP/1.1 server
capable of handling multiple concurrent clients, routing, file serving, and
gzip compression — all from scratch using Python's standard library.

> **Note:** If you're viewing this repo on GitHub, head over to
> [codecrafters.io](https://codecrafters.io) to try the challenge yourself.

---

## ✨ Features

- ⚡ **Concurrent request handling** via Python threads
- 🛣️ **Custom router** with support for static and wildcard routes
- 📦 **File upload & download** endpoints
- 🗜️ **Gzip compression** support via `Accept-Encoding` header
- 📋 **Request logging** with timestamps, status codes, and client info
- 🔧 Configurable **directory path** via CLI argument

---

## 🗂️ Project Structure

```
.
├── app/
│   ├── main.py           # Entry point — wires routes to the server
│   ├── routes.py         # Route handler (controller) functions
│   └── server/
│       ├── constant.py   # Server constants (HOST, PORT, CRLF, etc.)
│       ├── http.py       # HTTP request/response parsing & encoding
│       ├── log.py        # Request logger
│       ├── server.py     # Server & Route classes
│       └── utils.py      # CLI argument parsing & welcome message
├── codecrafters.yml      # CodeCrafters configuration
├── Pipfile               # Python dependencies
└── your_server.sh        # Shell script to start the server
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+**
- **Pipenv** (`pip install pipenv`)

### Installation

```sh
git clone https://github.com/rafnixg/codecrafters-http-server-python.git
cd codecrafters-http-server-python
pipenv install
```

### Running the Server

Start the server on the default host (`localhost`) and port (`4221`):

```sh
./your_server.sh
```

To serve files from a specific directory, pass the `--directory` flag:

```sh
./your_server.sh --directory /tmp/files
```

You should see output like:

```
Welcome to the HTTP server!
Listening on localhost:4221...
Press Ctrl+C to quit.

HTTP Compression is enabled: gzip

Available endpoints:
GET /
GET /echo/<message>
GET /user-agent
GET /files/<filename>
POST /files/<filename>
```

---

## 📡 API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Health check — returns `200 OK` |
| `GET` | `/echo/<message>` | Echoes `<message>` back in the response body |
| `GET` | `/user-agent` | Returns the `User-Agent` header sent by the client |
| `GET` | `/files/<filename>` | Downloads a file from the configured directory |
| `POST` | `/files/<filename>` | Uploads / creates a file in the configured directory |

### Examples

**Echo endpoint:**
```sh
curl http://localhost:4221/echo/hello
# Response: hello
```

**User-Agent endpoint:**
```sh
curl http://localhost:4221/user-agent
# Response: curl/7.x.x
```

**Gzip compression:**
```sh
curl -H "Accept-Encoding: gzip" http://localhost:4221/echo/hello --output - | gunzip
# Response: hello
```

**File upload:**
```sh
curl -X POST http://localhost:4221/files/test.txt --data "Hello, World!"
# Response: 201 Created
```

**File download:**
```sh
curl http://localhost:4221/files/test.txt
# Response: Hello, World!
```

---

## 🏗️ Architecture

The server is built around two core classes:

- **`Server`** — listens on a TCP socket, spawns a new thread per connection, and dispatches requests to the matching `Route`.
- **`Route`** — pairs an HTTP method + path pattern with a handler function. Supports exact matches and wildcard (`*`) suffix matching.

Request parsing and response encoding are handled by the **`Request`** and **`Response`** classes in `app/server/http.py`, which speak raw HTTP/1.1 over TCP.

---

## 🧑‍💻 CodeCrafters Submission

Push your changes to submit your solution:

```sh
git add .
git commit -m "implement stage"
git push origin master
```

Test output will be streamed to your terminal by CodeCrafters.

---

## 📄 License

This project is open source and available under the [MIT License](https://opensource.org/licenses/MIT).
