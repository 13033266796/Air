# coding：utf-8

from pymysql import *
import datetime
import time

def save_to_mysql(file_name, n):
    # with open(r"../history_data.txt",'r',encoding='utf-8') as f:
    with open(file_name, 'r', encoding='utf-8') as f:
        # data = f.readline()
        data = f.readline()
        i = n
        try:
            conn = connect(host='47.115.24.101', port=3306, user='root', passwd='123456', db='show_air',
                           charset='utf8')

            cursor1 = conn.cursor()
            # sql = 'TRUNCATE TABLE display_app_airinfo'
            # cursor1.execute(sql)

            while data:
                i += 1
                l = data.split(",") # 0,1,2,5
                # print(l)
                # date = l[1]
                # date_1 = datetime.datetime.strptime(l[1],'%Y-%m-%d').date()
                sql = 'INSERT INTO display_app_airinfo (id, city_name, city_date, city_AQI, city_PM2_5) VALUES ('+str(i)+','+ "'"+l[0]+"'"+ ","+"'"+l[1]+"'"+","+"'"+l[2]+"'"+","+"'"+l[3]+"'"+")"
                print(sql)
                cursor1.execute(sql)


                data = f.readline()
                # data =  False
            conn.commit()

        except Exception as e:
            print(e)
            conn.rollback()

        finally:
            cursor1.close()
            conn.close()


# try:
#     conn = connect(host='182.61.49.13', port=3306, user='root', passwd='123456', db='Show_Air', charset='utf8')
#     id = input("请输入id：")
#     name = input("请输入姓名：")
#     cursor1 = conn.cursor()
#
#     sql = 'INSERT INTO students (id,s_name) VALUES (%s,%s)'
#     cursor1.execute(sql, [id, name])
#     conn.commit()
#
#     cursor1.close()
#     conn.close()
# except Exception as e:
#     print(e)


# for i in range(1,6):
#     file_name = "../history_data_"+str(i)+".txt"
#     print(file_name)
#     save_to_mysql(file_name, i*10000)
#     time.sleep(10)

save_to_mysql("./original/history_data_202003.txt",70711)