def pint(num: int) -> str:
  try:
    num = int(num)
  except:
    raise TypeError("pint only accepts arguments that are type \"int\"")
  return "{:,}".format(num)