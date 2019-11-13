#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
import namegenerator
import hashlib as hasher
import torch
import syft


# In[2]:


hook = syft.TorchHook(torch)
names = list()
transaction = list()
labels = list()


# In[3]:


i = 0
while i < 50:
    name = namegenerator.gen()
    names.append(name)
    transaction_id = random.randint(100000000000000,999999999999999)
    transaction.append(transaction_id)
    label = random.randint(0,1)
    labels.append(label)
    i = i + 1


# In[4]:

print("*************** All names, Transaction_id , labels  *********************")

for i in range(20):
    print( "Name -->",names[i] , "Transaction id -->:",transaction[i], "Label -->",labels[i])


# In[5]:


class Block:
    def __init__(self, name, transaction_id,label):
        self.name = name
        self.transaction_id = transaction_id
        self.label = label
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hasher.sha256()
        sha.update(str(self.name).encode('utf-8') +
                   str(self.transaction_id).encode('utf-8') +
                   str(self.label).encode('utf-8'))
        return sha.hexdigest()


# In[6]:


name_0 = names[0]
transaction_0 = transaction[0]
labels_0 = labels[0]
print("********* First Block details *****************")
print("name",name_0,"transaction",transaction_0,"labels",labels_0)


# In[7]:


def create_genesis_block():

    return Block(name_0, transaction_0,labels_0)


# In[8]:


def next_block(last_block,j):
    this_name = names[j]
    this_transaction_id = transaction[j]
    this_label = labels[j]
    this_hash = last_block.hash
    return Block(this_name, this_transaction_id,label)


# In[9]:


blockchain = [create_genesis_block()]
previous_block = blockchain[0]
num_of_blocks_to_add = len(names)


# In[20]:


print("************************** All block details ****************************")

for i in range(0, num_of_blocks_to_add):
    block_to_add = next_block(previous_block,i)
    blockchain.append(block_to_add)
    previous_block = block_to_add
    print("Name: {}\n".format(block_to_add.name))
    print("Hash: {}\n".format(block_to_add.transaction_id))
    print("Hash: {}\n".format(block_to_add.label))
    print("Hash: {}\n".format(block_to_add.hash))


# In[11]:


a = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","aa","bb","cc",
     "dd","ee","ff","gg","hh","ii","jj","kk","ll","mm","nn","oo","pp","qq","rr","ss","tt","uu","vv","ww","xx"]


# In[12]:


b = a


# In[13]:


for i in range(len(names)):
    names[i] = syft.VirtualWorker(hook, id = names[i])
    a[i] = torch.tensor([transaction[i]]).send(names[i])
    b[i] = torch.tensor([labels[i]]).send(names[i])


# In[22]:

print("************ Pointers of transaction_id and labels ***************************")

for i in range(len(a)):
    print("Transaction_id address -->", a[i],"\n Label address -->",b[i])


# In[23]:


datasets = []


# In[24]:


for i in range(len(names)):
    datasets.append((a[i],b[i]))


# In[25]:

print("******************************** datasets values ***********************************")

for i in range(10):
    print(datasets[i])


# In[17]:


from torch import nn
from torch import optim


# In[18]:


def train(iterations = 20):
    model = nn.Linear(50,22)
    optimizer_fed = optim.SGD(params = model.parameters(), lr = 0.1)
    for iter in range(iterations):
        for data, target  in datasets:
            model = model.send(data.location)
            optimizer_fed.zero_grad()
            pred = model(data)
            loss = (( pred - target) ** 2).sum()
            loss.backward()
            optimizer_fed.step()
            model = model.get()
            print(loss.get())


# In[19]:


train()


# In[ ]:
