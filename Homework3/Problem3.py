import numpy as np
import matplotlib.pyplot as plt

mu = np.matrix([1,4]).T
cov = np.matrix([[2,1.5],[1.5,6]])

def para_calculator(mu, cov):
    mu1 = mu.item(0)
    mu2 = mu.item(1)
    s1 = cov.item((0,0))
    s2 = cov.item((1,1))
    rho = cov.item((0,1))
    
    mu0 = (mu1*s2+mu2*s1-(mu1+mu2)*rho)/(s1+s2-2*rho)
    s0 = (s1*s2-rho)/(s1+s2-2*rho)
    k = (s1+s2-2*rho)/(mu1-mu2)**2
    
    return mu0, s0, k

def CML(mu, cov, Rf):
           
    inv = np.linalg.inv(cov)
    u = np.matrix([1,1]).T

    A = u.T@inv@u
    B = u.T@inv@mu
    C = mu.T@inv@mu
    
    mu0 = para_calculator(mu, cov)[0] 
    
    if Rf == mu0:
        slope = np.sqrt((A@C - B**2)/A)
        mu_m = Rf
    else:       
        w = inv@(mu - Rf*u) / (B-A*Rf)
        mu_m = mu.T@w
        s_m = (A@mu_m**2-2*B*mu_m+C)/(A@C-(B**2))
        slope = (mu_m - Rf)/np.sqrt(s_m)   
    
    return mu_m, slope

mu0, s0, k = para_calculator(mu, cov)
Rf = mu0 - 1
mu_m, slope = CML(mu, cov, Rf)

x = np.linspace(0, 8, 500)
y = np.linspace(-5, 15, 500)
sp = np.linspace(0, 8, 9)
cml = []
cml_neg = []
for i in range(len(sp)):
    cml.append(Rf + sp[i] * slope.item(0))
    cml_neg.append(Rf - sp[i] * slope.item(0))

x, y = np.meshgrid(x, y)
plt.contour(x, y, ((y-mu0)**2 - (x**2-s0)/k), [0], colors='b')
plt.plot(cml, color = 'black', ls = '--')
plt.plot(cml_neg, color = 'black', ls = '--')
plt.title('$R_{f} < \mathrm{E}[R_{GMV}],\ R_{f} = 0.3,\ \mathrm{E}[R_{GMV}] = 1.3$')
plt.ylabel('$\mu$')
plt.xlabel('$\sigma$')
plt.show()

Rf = mu0 + 1
mu_m, slope = CML(mu, cov, Rf)

x = np.linspace(0, 8, 500)
y = np.linspace(-5, 15, 500)
sp = np.linspace(0, 8, 9)
cml = []
cml_neg = []
for i in range(len(sp)):
    cml.append(Rf + sp[i] * slope.item(0))
    cml_neg.append(Rf - sp[i] * slope.item(0))

x, y = np.meshgrid(x, y)
plt.contour(x, y, ((y-mu0)**2 - (x**2-s0)/k), [0], colors='b')
plt.plot(cml, color = 'black', ls = '--')
plt.plot(cml_neg, color = 'black', ls = '--')
plt.title('$R_{f} > \mathrm{E}[R_{GMV}],\ R_{f} = 2.3,\ \mathrm{E}[R_{GMV}] = 1.3$')
plt.ylabel('$\mu$')
plt.xlabel('$\sigma$')
plt.show()

Rf = mu0 
mu_m, slope = CML(mu, cov, Rf)

x = np.linspace(0, 8, 500)
y = np.linspace(-5, 15, 500)
sp = np.linspace(0, 8, 9)

cml = []
cml_neg = []
for i in range(len(sp)):
    cml.append(Rf + sp[i] * slope.item(0))
    cml_neg.append(Rf - sp[i] * slope.item(0))

x, y = np.meshgrid(x, y)
plt.contour(x, y, ((y-mu0)**2 - (x**2-s0)/k), [0], colors='b')
plt.plot(cml, color = 'black', ls = '--')
plt.plot(cml_neg, color = 'black', ls = '--')
plt.title('$R_{f} = \mathrm{E}[R_{GMV}],\ R_{f} = 1.3,\ \mathrm{E}[R_{GMV}] = 1.3$')
plt.ylabel('$\mu$')
plt.xlabel('$\sigma$')
plt.show()