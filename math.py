import os
import math
from discord.ext import commands
import discord
import random 
from dotenv import load_dotenv
from discord.ext.commands import Bot

bot = Bot("!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('TestBot is online')
    

def simpleCheck(equation):
    return True


def checker(equation):
    count = 0
    first_node = 0
    last_node = 0
    while count < len(equation):
        if equation[count] == '(':
            first_node = count
            break
        count += 1
    count = len(equation) - 1
    while count != 0:
        if equation[count] == ')':
            last_node = count
            break
        count -= 1
    count = first_node + 1
    new_equation = []
    while count < last_node:
        new_equation.append(equation[count])
        count += 1
    result_equation = checker(new_equation)
    simplified_equation = []
    count = 0
    while count < first_node:
        simplified_equation.append(equation[count])
        count += 1
    print(simplified_equation)
    simplified_equation.append(result_equation)
    count = second_node
    while count < (len(equation) - 1):
        simplified_equation.append(equation[count])
        count += 1
    print(simplified_equation)
    print(new_equation)
    if '^' in equation:
        equation = exponent(equation)
    if '*' in equation:
        equation = multiply(equation)
    if '/' in equation:
        equation = divide(equation)
    if '+' in equation:
        equation = add(equation)
    if '-' in equation:
        equation = subtract(equation)
    return equation[0]


def exponent(equation):         #do an additional check for the exponents of exponents
    count = 1
    while count < len(equation):
        if equation[count] == '^':
            equation[count + 1] = pow(float(equation[count -1]),float(equation[count + 1]))
            equation.pop(count - 1)
            equation.pop(count - 1)
            count = 0
            print(equation)
        count+=1
    return equation


def multiply(equation):
    count = 1
    while count < len(equation):
        if equation[count] == '*':
            result = float(equation[count-1]) * float(equation[count + 1])
            equation[count + 1] = result
            equation.pop(count - 1)
            equation.pop(count - 1)
            count = 0
            print(equation)
        count+=1
    return equation


def divide(equation):
    count = 1
    while count < len(equation):
        if equation[count] == '/':
            result = float(equation[count-1]) / float(equation[count + 1])
            equation[count + 1] = result
            equation.pop(count - 1)
            equation.pop(count - 1)
            count = 0
            print(equation)
        count+=1
    return equation


def add(equation):
    count = 1
    while count < len(equation):
        if equation[count] == '+':
            result = float(equation[count-1]) + float(equation[count + 1])
            equation[count + 1] = result
            equation.pop(count - 1)
            equation.pop(count - 1)
            count = 0
            print(equation)
        count+=1
    return equation


def subtract(equation):
    count = 1
    while count < len(equation):
        if equation[count] == '-':
            result = float(equation[count-1]) - float(equation[count + 1])
            equation[count + 1] = result
            equation.pop(count - 1)
            equation.pop(count - 1)
            count = 0
            print(equation)
        count+=1
    return equation


@bot.command()
async def equation(ctx, *args):
    equation = list(args)
    if not simpleCheck(equation):
        ctx.send("The equation sent in not a valid simple equation. Try again.")
    result = checker(equation)
    #if '^' in equation:
    #    equation = exponent(equation)
    #if '*' in equation or '/' in equation:
    #    equation = multdiv(equation)
    #if '+' in equation or '-' in equation:
    #    equation = addsub(equation)
    #print(equation)
    await ctx.send(result[0])



bot.run("MTA2NzAwNzg2ODU1OTE3NTcxMA.GVgbT5.pLTh-Yfbo7lMDHgCnitRgqoHDdWnNcjOPjcVUI")  #TOKEN