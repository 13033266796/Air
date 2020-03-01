with open(r"./DataProcessing/display_app_airinfo.txt","r",encoding="utf-8") as f:
    data = f.readline()
    i = 1
    j = 1
    while data :
        data = data.split(",")
        data[-1] = data[-1].replace("\n","")
        # print(data)
        # print(",".join(data[1:]))
        data = ",".join(data[1:])
        if j > 10000:
            j = 1
            i += 1
        file_name = "history_data_"+str(i-1)+".txt"
        with open(file_name,"a",encoding="utf-8") as t:
            t.write(data+"\n")
        j += 1
        data = f.readline()