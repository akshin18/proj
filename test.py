import jwt

JWT_SECRET_KEY = "de6be753cf4e8f3016ddf58a8013cdd0eef62bcfc630e65f3b1e26375eea81bc5ce20c1949137d2d"


token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJfaWQiOiI2M2JlMDA2OTUzNGUyNzQwODQ4M2NhZmQiLCJwb3NpdGlvbiI6MSwidGltZSI6IjA4LjAyLjIwMjMgMDE6MzM6MDUifQ.AW2N5-Is7-oMdxlrKnddar6K_n1qPj2zSQPYD8Wy9j9UKODymlKR0UIJ2oTl-dbFaGC2luUtGEwbbCFLcNuy_w"

claims = jwt.decode(token.strip(), JWT_SECRET_KEY, algorithms=["HS512"])
print(claims)
