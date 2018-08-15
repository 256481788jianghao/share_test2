import pandas as pd

pd.set_option('display.width',1000)

def c_fun(n,x):
    #return (x**n) * (x-1) / (x**n -1)
    return (x**(n+1) - x**n )/(x**n - 1)

def find_x(n,target,step=1e-7,delta=1e-7,max_step=int(1e7)):
    x = 1
    d = 0
    ans = 0
    for i in range(0,max_step):
        x = x+step
        ans = c_fun(n,x)
        d = ans - target
        #print(x,ans,d)
        if abs(d) < delta:
            return x,ans,d
    return x,ans,d

def make_target(n,k):
    return (1+k)/n

#print(find_x(18,make_target(18,1080/8000)))
ans_dict={}
for n in range(3,27,3):
    tmplist = []
    for k in range(1,21):
        k_in = k*0.005
        x,ans,d = find_x(n,make_target(n,k_in))
        #print(x,d)
        tmplist.append((x**12-1)*100)
    key = 'M'
    if n < 10:
        key = key +'0'+str(n)
    else:
        key = key+str(n)
    ans_dict[key] = tmplist

tmpKlist = []
for k in range(1,21):
    k_in = k* 0.005
    tmpKlist.append(k_in)
    
ans_dict['K'] = tmpKlist

print(pd.DataFrame(ans_dict))

#print((1+1e-7)**24-1)

