from sqlmodel import SQLModel, Field

#wer benutzt die App
class User(SQLModel, table=True):
    # DB vergibt ID automatisch mit default=None
    id: int = Field(default=None, primary_key=True)

    email: str = Field(index=True, unique=True)

    #einfaches Textfeld, keine Einschränkungen
    password: str