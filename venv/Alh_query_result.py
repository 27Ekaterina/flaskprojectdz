from orm_db import Session, Area, Where_search, Skill, WordSkill, Word


cur = Session()
res = cur.query(WordSkill).all()
for i in res:
    print(i)
