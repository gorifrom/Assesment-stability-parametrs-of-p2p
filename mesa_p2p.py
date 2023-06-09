# -*- coding: utf-8 -*-
"""mesa p2p.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14E9rhw8hi_lNR7AZDvBMW5dyzSNIxOMa
"""

! pip install mesa

import numpy as np
import pandas as pd
from tqdm import tqdm
import scipy.stats as sts
import re
import datetime
import time

import matplotlib.pyplot as plt
import seaborn as sns
from pylab import rcParams

plt.style.use('fivethirtyeight')
rcParams['figure.figsize'] = 12, 6

import warnings
warnings.filterwarnings("ignore")
        
import mesa
import random



def compute_gini(model):
    agent_wealths = [agent.wealth for agent in model.schedule.agents]
    x = sorted(agent_wealths)
    N = model.num_agents
    B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
    return 1 + (1 / N) - 2 * B

class Agent(mesa.Agent):
    def __init__(self, unique_id, model, p, r):
        super().__init__(unique_id, model)
        self.p = p
        self.r = r
        # Бедные
        self.wealth = 0
        self.debitor = False
        # Богатые
        if sts.bernoulli.rvs(p) == 1:
            self.wealth = 500
            

    def step(self):
        # Базовый безусловный доход
        self.wealth += 5
        # Базовая аренда 40 каждые 10 дней
        if i % 10 == 0:
            self.wealth -= 40
        # Возврат кредита 50 если настало время возврата
        if self.debitor == True:
            if self.credit_time >= i:
                if sts.bernoulli.rvs(r) == 0:
                    self.creditor.wealth += 50
                    self.wealth -= 50
                    self.debitor = False
                else:
                    self.debitor = False
        # Кредиты только для бедных
        if self.wealth > 40:
        # Кредиты только для бедных
            return
        # Случайный партнер
        creditor = self.random.choice(self.model.schedule.agents)
        # Только богатый дает кредит
        if creditor.wealth < 200:
            return
        # Дает кредит 40, но вернуть надо 50 через 10 шагов
        creditor.wealth -= 40
        self.wealth += 40        
        # Надо вернуть 50 через 10 шагов
        self.debitor = True
        self.creditor = creditor
        self.credit_time = i + 10
        
class Model(mesa.Model):
    def __init__(self, N, p, r):
        self.num_agents = N
        self.schedule = mesa.time.RandomActivation(self)
        # Создать агентов
        for i in range(self.num_agents):
            a = Agent(i, self, p, r)
            self.schedule.add(a)
        # Создать дата-коллектор
        self.datacollector = mesa.DataCollector(
            model_reporters={"Gini": compute_gini}, 
            agent_reporters={"Wealth": "wealth"})

    def step(self):
        self.datacollector.collect(self)            
        self.schedule.step()

N = 100
N_step = 1000
p = 0.3
r = 0.15
model = Model(N, p, r)
            
for i in range(N_step):
    model.step()

gini = model.datacollector.get_model_vars_dataframe()
gini.plot();
plt.title(f'График устойчивости при p={p}, r={r}, n={N}, N={N_step}', pad=1);
plt.xlabel('Шаг моделирования (N)');
plt.ylabel('Коэффициент Джини(k)');

gini_0 = gini

gini_1 = gini

gini_2 = gini

gini_3 = gini

gini_4 = gini

plt.plot(gini_0, label='r=0.15, I = 0.35')
plt.plot(gini_1, label='r=0.15, I = 0.325')
plt.plot(gini_2, label='r=0.15, I = 0.3')
plt.plot(gini_3, label='r=0.15, I = 0.275')
plt.plot(gini_4, label='r=0.15, I = 0.25')

plt.title(f'График устойчивости при p={p}, n={N}, N={N_step}', pad=1.4);
plt.xlabel('Шаг моделирования(N)');
plt.ylabel('Коэффициент Джини (k)');
plt.legend();







agent_wealth = model.datacollector.get_agent_vars_dataframe()
agent_wealth.head(60)

agent_wealth.xs(14, level="AgentID")

agent_wealth.info()

agent_wealth = [a.wealth for a in ]
plt.hist(agent_wealth);

