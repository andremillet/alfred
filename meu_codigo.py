
# Arquivo de exemplo para testar o Alfred

def somar_com_loop(lista=list(range(1000))):
    """Soma os números de uma lista usando um loop for."""
    total = 0
    for numero in lista:
        total += numero
    return total

def somar_com_sum(lista=list(range(1000))):
    """Soma os números de uma lista usando a função nativa sum()."""
    return sum(lista)

# Uma função um pouco mais complexa para sugestões
def encontrar_pares(numeros=list(range(1000))):
    """Encontra todos os números pares em uma lista."""
    pares = []
    for numero in numeros:
        if numero % 2 == 0:
            pares.append(numero)
    return pares
