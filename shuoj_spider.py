from urllib import request

if __name__=="__main__":
    base = "http://acmoj.shu.edu.cn/problem/"
    for i in range(1,427):
        url = base+str(i)+'/'
        url_req = request.Request(url)
        url_response = request.urlopen(url_req)
        url_html = url_response.read()
        with open('problem\\'+str(i)+".html", "wb") as f:
            f.write(url_html)
    print("完成")