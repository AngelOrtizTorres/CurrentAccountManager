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
        deposit_query = "SELECT id, importe, fecha_hora, concepto FROM movements WHERE tipo = %s AND numero_cuenta = %s"
        params = ('ingreso', number_account)
        cursor.execute(deposit_query, params)
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
        withdraw_query = "SELECT id, importe, fecha_hora, concepto FROM movements WHERE tipo = %s AND numero_cuenta = %s"
        params = ('salida', number_account)
        cursor.execute(withdraw_query, params)
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
        transfer_query = "SELECT id, importe, fecha_hora, tipo, cuenta_transferencia, concepto FROM movements WHERE (tipo = %s OR tipo = %s) AND numero_cuenta = %s"
        params = ('transferencia enviada', 'transferencia recibida', number_account)
        cursor.execute(transfer_query, params)
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
    while True:
        try:
            number_account = int(input("Introduce el número de cuenta: "))
            break
        except Exception as e:
            print(f"Error: {e}")

    while True:
        try:
            start_date_str = input("Introduce la fecha inicial (YYYY-MM-DD): ")
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            break
        except Exception as e:
            print(f"Formato incorrecto de fecha. Usa YYYY-MM-DD.")

    while True:
        try:
            end_date_str = input("Introduce la fecha final (YYYY-MM-DD): ")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            if end_date < start_date:
                print("La fecha final debe ser igual o posterior a la inicial.")
                continue
            break
        except Exception as e:
            print(f"Formato incorrecto de fecha. Usa YYYY-MM-DD.")

    cursor = mysql_movements.connection.cursor()
    try:
        movements_query = """
            SELECT id, importe, fecha_hora, tipo, cuenta_transferencia, concepto
            FROM movements
            WHERE numero_cuenta = %s AND fecha_hora BETWEEN %s AND %s
            ORDER BY fecha_hora DESC
        """
        params = (number_account, start_date_str + " 00:00:00", end_date_str + " 23:59:59")
        cursor.execute(movements_query, params)
        movements = cursor.fetchall()

        print(f"\nMovimientos de la cuenta {number_account:010} desde {start_date_str} hasta {end_date_str}")
        print("-------------------------------------------------------------------------------------------------------")
        print(" ID  | Importe   | Fecha y Hora        | Tipo                  | Cuenta Transferencia | Concepto")
        print("-------------------------------------------------------------------------------------------------------")

        for move in movements:
            id_, importe, fecha, tipo, cuenta_transf, concepto = move
            cuenta_transf_str = f"{cuenta_transf:010}" if cuenta_transf else "N/A"
            print(f"{id_:<4} | {float(importe):>8.2f}€ | {fecha.strftime('%Y-%m-%d %H:%M:%S')} | {tipo:<22} | {cuenta_transf_str:^20} | {concepto}")

        print()

    except Exception as e:
        print(f"Error al consultar los movimientos: {e}")
    finally:
        cursor.close()