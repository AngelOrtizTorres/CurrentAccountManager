from datetime import datetime

def get_all_deposit(mysql_movements):
    while True:
        try:
            number_account = int(input("Introduce el número de cuenta para ver los ingresos: "))
            break
        except Exception as e:
            print(f"Error: {e}")

    cursor = mysql_movements.connection.cursor()
    try:
        query = "SELECT id, importe, fecha_hora, concepto FROM movements WHERE tipo = %s AND numero_cuenta = %s"
        params = ('ingreso', number_account)
        cursor.execute(query, params)
        deposits = cursor.fetchall()
        
        print(f"\nIngresos de la cuenta {number_account:010}")
        print("---------------------------------------------------------------")
        print(" ID  | Importe   | Fecha y Hora        | Concepto")
        print("---------------------------------------------------------------")

        for deposit in deposits:
            id_, importe, fecha, concepto = deposit
            print(f"{id_:<4} | {float(importe):>8.2f}€ | {fecha.strftime('%Y-%m-%d %H:%M:%S')} | {concepto}")

        print()
            
    except Exception as e:
        print(f"Error al consultar las cuentas: {e}")
    finally:
        cursor.close()

def get_all_withdraw(mysql_movements):
    while True:
        try:
            number_account = int(input("Introduce el número de cuenta para ver los retiros: "))
            break
        except Exception as e:
            print(f"Error: {e}")

    cursor = mysql_movements.connection.cursor()
    try:
        query = "SELECT id, importe, fecha_hora, concepto FROM movements WHERE tipo = %s AND numero_cuenta = %s"
        params = ('salida', number_account)
        cursor.execute(query, params)
        withdraws = cursor.fetchall()
        
        print(f"\nRetiros de la cuenta {number_account:010}")
        print("---------------------------------------------------------------")
        print(" ID  | Importe   | Fecha y Hora        | Concepto")
        print("---------------------------------------------------------------")

        for withdraw in withdraws:
            id_, importe, fecha, concepto = withdraw
            print(f"{id_:<4} | {float(importe):>8.2f}€ | {fecha.strftime('%Y-%m-%d %H:%M:%S')} | {concepto}")

        print()
            
    except Exception as e:
        print(f"Error al consultar las cuentas: {e}")
    finally:
        cursor.close()

def get_all_transfer(mysql_movements):
    while True:
        try:
            number_account = int(input("Introduce el número de cuenta para ver las transferencias: "))
            break
        except Exception as e:
            print(f"Error: {e}")

    cursor = mysql_movements.connection.cursor()
    try:
        query = "SELECT id, importe, fecha_hora, tipo, cuenta_transferencia, concepto FROM movements WHERE (tipo = %s OR tipo = %s) AND numero_cuenta = %s"
        params = ('transferencia enviada', 'transferencia recibida', number_account)
        cursor.execute(query, params)
        transfers = cursor.fetchall()
        
        print(f"\nTransferencias de la cuenta {number_account:010}")
        print("-------------------------------------------------------------------------------------------------------")
        print(" ID  | Importe   | Fecha y Hora        | Tipo                   | Cuenta Transferencia | Concepto")
        print("-------------------------------------------------------------------------------------------------------")

        for transfer in transfers:
            id_, importe, fecha, tipo, cuenta_transf, concepto = transfer
            cuenta_transf_str = f"{cuenta_transf:010}" if cuenta_transf else "N/A"
            print(f"{id_:<4} | {float(importe):>8.2f}€ | {fecha.strftime('%Y-%m-%d %H:%M:%S')} | {tipo:<22} | {cuenta_transf_str:^20} | {concepto}")

        print()
            
    except Exception as e:
        print(f"Error al consultar las cuentas: {e}")
    finally:
        cursor.close()

def get_movements_betweeen_date(mysql_movements):
    pass