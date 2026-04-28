from sqlalchemy import text

def ins_query(req, db):
    db.execute(
        text("""
                INSERT INTO TEST(name, age) values(:name, :age)
            """
        ),
        {
            "name" : req.name,
            "age" : req.age
        }
    )
        
def sel_query(req, db):
    result = db.execute(
            text("""
                 SELECT ID, NAME, AGE FROM TEST WHERE id = :id
                 """),
                {
                    "id" : req.id
                }
        )
        
    print(f"###### result : {result} ######")
    print(f"###### result_type : {type(result)} ######")
    
    rows = [dict(row) for row in result.mappings().all()]
    
    print(f"###### rows : {rows} ######")
    print(f"###### rows_type: {type(rows)} ######")
    
    return rows

def put_query(req, db):
    db.execute(
            text("""
                    UPDATE TEST SET name = :name, age = :age WHERE id = :id
                 """),
                {
                    "id" : req.id,
                    "name" : req.name,
                    "age" : req.age
                }
        )
    
# def patch_query(req, db):