
# funsción para calcular escenario marginación
def get_escenario(monto_estimado, monto_limite):
  '''
    input :
      monto_estimado : lista 
      monto_limite   : presupuesto asignado a un producto para un año en particular
    output
      montos : lista de montos estimados que no superan el limite de presupuesto 
  '''
  monto = 0
  montos_list = [] 
  for monto_i in monto_estimado:
    if monto <= monto_limite:
      monto = monto + monto_i
      montos_list.append(monto_i)
    else:
      montos_list.append(0)

  return montos_list