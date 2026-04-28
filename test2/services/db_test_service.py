from repositories import db_test
from fastapi.responses import JSONResponse
from fastapi import status
from core.exceptions import AppException

def insert_test(req, db):
    try:
        raise Exception
        db_test.ins_query(req, db)
        
        db.commit()
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message" : "insert success"
            }
        )
    except Exception as e :
        db.rollback()
        print(f"exception : {e}")
        raise
        
def select_test(req, db):
    try:
        raise AppException("일단 오류 발생", status.HTTP_400_BAD_REQUEST)
        rows = db_test.sel_query(req, db)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message" : "select success",
                "data" : rows
            }
        )
    except AppException:
        print("### checkpoint1 ###")
        raise AppException("hello error", status.HTTP_400_BAD_REQUEST)
    except Exception as e :
        print("### checkpoint2 ###")
        db.rollback()
        print(f"exception : {e}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "message" : "select fail"
            }
        )
        
def put_test(req, db):
    try:
        db_test.put_query(req, db)
        
        db.commit()
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message" : "put success"
            }
        )
    except Exception as e :
        db.rollback()
        print(f"exception : {e}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "message" : "put fail"
            }
        )
        
# def patch_test(req, db):
#     try:
#         ## old version
#         # upd_cols = []
#         # upd_vals = []
        
#         data = req.model_dump(exclude_unset=True)
        
#         print(f"##### data : {data} #####")
        
#         ## new version
#         if "id" not in data:
#             return JSONResponse(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             content={
#                 "message" : "id가 필요합니다."
#             }
#         )
            
#         id_value = data.pop("id")
        
#         if not data:
#             return JSONResponse(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 content={
#                     "message" : "수정할 값이 없습니다."
#                 }
#             )
            
#         bind_params = {**data, "id":id_value}
        
#         upd_clause = ", ".join([f"{key} = :{key}" for key in data.keys()])
        
#         db.execute(
#             text(f"""
#                     UPDATE TEST SET {upd_clause} WHERE id = :id
#                  """),
#                 bind_params
#         )
        
        
#         ## old version
#         # upd_query = ""
#         # upd_bind = {}
        
#         # if upd_cols:    
            
#         #     for upd_col, upd_val in zip(upd_cols, upd_vals):
#         #         if upd_query :
#         #            upd_query += ", " 
                   
#         #         if upd_col != "id":
#         #             upd_query += f"{upd_col} = :{upd_col}"
                
#         #         upd_bind[upd_col] = upd_val
                
        
#         # print(f"##### upd_query : {upd_query} #####")
#         # print(f"##### upd_bind : {upd_bind} #####")
        
#         # t_text = f"""
#         #             UPDATE TEST SET {upd_query} WHERE id = :id
#         #          """
                 
#         # print(f"##### t_text : {t_text} #####")
        
#         # db.execute(
#         #     text(f"""
#         #             UPDATE TEST SET {upd_query} WHERE id = :id
#         #          """),
#         #             upd_bind
#         # )
        
#         db.commit()
        
#         return JSONResponse(
#             status_code=status.HTTP_200_OK,
#             content={
#                 "message" : "patch success"
#             }
#         )
#     except Exception as e :
#         db.rollback()
#         print(f"exception : {e}")
#         return JSONResponse(
#             status_code=status.HTTP_404_NOT_FOUND,
#             content={
#                 "message" : "patch fail"
#             }
#         )