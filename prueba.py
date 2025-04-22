from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import init_db, get_db_connection
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Inicializar la base de datos
init_db()

conn = get_db_connection()
cursor = conn.cursor()


# Verificar si existen citas en la base de datos
cursor.execute('SELECT COUNT(*) FROM citas')
if cursor.fetchone()[0] == 0:
    # Asignar 5 citas únicas a cada doctor
    cursor.execute('SELECT id FROM doctores ORDER BY id')
    doctor_ids = [row[0] for row in cursor.fetchall()]
    for doctor_id in doctor_ids:
        for i in range(5):
            fecha = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d %H:%M:%S')
            cubiculo = f'Cubículo {i + 1}'
            cursor.execute('''
                INSERT INTO citas (doctor_id, fecha, cubiculo, estado)
                VALUES (%s, %s, %s, %s)
            ''', (doctor_id, fecha, cubiculo, 'Disponible'))

conn.commit()
conn.close()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        # Verificar credenciales en la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        conn.close()

        if account:
            session['loggedin'] = True
            session['username'] = account[1]
            session['role'] = account[3]
            if account[3] == 'user':
                return redirect(url_for('user_menu'))
            elif account[3] == 'doctor':  # Redirigir al menú de doctor
                return redirect(url_for('doctor_menu'))
        else:
            msg = '¡Usuario o contraseña incorrectos!'
    return render_template('login.html', msg=msg)

@app.route('/user_menu', methods=['GET', 'POST'])
def user_menu():
    if 'loggedin' in session and session.get('role') == 'user':
        if request.method == 'POST':
            option = request.form.get('option')
            if option == '1':
                return redirect(url_for('agendar_cita'))
            elif option == '2':
                return redirect(url_for('ver_citas'))
            elif option == '3':
                return redirect(url_for('cancelar_citas'))
            elif option == '4':
                return redirect(url_for('mi_perfil'))
            elif option == '5':
                return redirect(url_for('mis_ordenes'))
            elif option == '6':
                return redirect(url_for('logout'))
        return render_template('user_menu.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/agendar_cita', methods=['GET', 'POST'])
def agendar_cita():
    if 'loggedin' in session and session.get('role') == 'user':
        conn = get_db_connection()
        cursor = conn.cursor()

        if request.method == 'POST':
            numero_orden = request.form.get('numero_orden')
            doctor_id = request.form.get('doctor_id')

            # Verificar si el número de orden existe en la base de datos
            if numero_orden:
                cursor.execute('SELECT descripcion FROM ordenes WHERE descripcion = %s', (numero_orden,))
                orden = cursor.fetchone()

                if not orden:
                    # Redirigir a los doctores de Medicina General si la orden no es válida
                    cursor.execute('SELECT id, nombre, apellido FROM doctores WHERE especialidad = "Medicina General"')
                    doctores = cursor.fetchall()
                    conn.close()
                    return render_template('agendar_cita.html', doctores=doctores, especialidad="Medicina General", citas=None)

                # Determinar la especialidad basada en el número de orden
                especialidad_codigos = {
                    '01': 'Cardiología',
                    '02': 'Pediatría',
                    '03': 'Ginecología',
                    '04': 'Neurología',
                    '05': 'Psiquiatría'
                }
                especialidad = especialidad_codigos.get(numero_orden[:2], None)

                if not especialidad:
                    # Redirigir a los doctores de Medicina General si la especialidad no es válida
                    cursor.execute('SELECT id, nombre, apellido FROM doctores WHERE especialidad = "Medicina General"')
                    doctores = cursor.fetchall()
                    conn.close()
                    return render_template('agendar_cita.html', doctores=doctores, especialidad="Medicina General", citas=None)

                # Obtener la lista de doctores de la especialidad
                cursor.execute('SELECT id, nombre, apellido FROM doctores WHERE especialidad = %s', (especialidad,))
                doctores = cursor.fetchall()

                conn.close()
                return render_template('agendar_cita.html', doctores=doctores, especialidad=especialidad, citas=None)

            # Verificar si se seleccionó un doctor para mostrar sus citas disponibles
            if doctor_id:
                cursor.execute('''
                    SELECT id, fecha, cubiculo
                    FROM citas
                    WHERE doctor_id = %s AND estado = 'Disponible'
                    ORDER BY fecha
                ''', (doctor_id,))
                citas = cursor.fetchall()

                # Obtener información del doctor seleccionado
                cursor.execute('SELECT nombre, apellido FROM doctores WHERE id = %s', (doctor_id,))
                doctor = cursor.fetchone()

                conn.close()
                return render_template('agendar_cita.html', doctores=None, especialidad=None, citas=citas, doctor=doctor)

        conn.close()
        return render_template('agendar_cita.html', doctores=None, especialidad=None, citas=None, doctor=None)
    
@app.route('/orden_no_valida', methods=['GET', 'POST'])
def orden_no_valida():
    if 'loggedin' in session and session.get('role') == 'user':
        conn = get_db_connection()
        cursor = conn.cursor()

        # Obtener los nombres de los doctores de Medicina General
        cursor.execute('SELECT id, nombre FROM doctores WHERE especialidad = "Medicina General"')
        doctores = cursor.fetchall()

        agenda = []
        if request.method == 'POST':
            doctor_id = request.form.get('doctor_id')
            if doctor_id:
                # Obtener la agenda del doctor seleccionado
                cursor.execute('''
                    SELECT id, fecha, cubiculo, estado
                    FROM citas
                    WHERE doctor_id = %s AND estado = 'Disponible'
                    ORDER BY fecha
                ''', (doctor_id,))
                agenda = cursor.fetchall()
                conn.close()  # Cerrar la conexión después de obtener la agenda
                return render_template('agenda_doctor.html', agenda=agenda, doctor_id=doctor_id)

        conn.close()  # Cerrar la conexión si no se selecciona un doctor
        return render_template('orden_no_valida.html', doctores=doctores)
    return redirect(url_for('login'))

@app.route('/seleccionar_cita/<int:cita_id>', methods=['POST'])
def seleccionar_cita(cita_id):
    if 'loggedin' in session and session.get('role') == 'user':
        conn = get_db_connection()
        cursor = conn.cursor()

        # Eliminar citas duplicadas antes de proceder
        cursor.execute('''
            DELETE FROM citas
            WHERE id NOT IN (
                SELECT MIN(id)
                FROM citas
                GROUP BY fecha, cubiculo, doctor_id
            )
        ''')

        # Obtener el ID del usuario actual
        cursor.execute('SELECT id, cliente_id FROM usuarios WHERE username = %s', (session['username'],))
        user = cursor.fetchone()
        if not user:
            conn.close()
            flash('Error al obtener el ID del usuario.')
            return redirect(url_for('agendar_cita'))
        usuario_id, cliente_id = user

        # Verificar si la cita está disponible
        cursor.execute('SELECT estado, doctor_id FROM citas WHERE id = %s', (cita_id,))
        cita = cursor.fetchone()
        if cita and cita[0] == 'Disponible':
            doctor_id = cita[1]

            # Verificar si el doctor pertenece a "Medicina General"
            cursor.execute('SELECT especialidad FROM doctores WHERE id = %s', (doctor_id,))
            especialidad = cursor.fetchone()
            if especialidad and especialidad[0] != "Medicina General":
                # Verificar si el usuario tiene una orden válida para otras especialidades
                cursor.execute('SELECT id FROM ordenes WHERE cliente_id = %s', (cliente_id,))
                orden = cursor.fetchone()
                if not orden:
                    conn.close()
                    flash('No tienes una orden válida para agendar esta cita.')
                    return redirect(url_for('agendar_cita'))

                # Marcar la orden como expirada eliminándola
                cursor.execute('DELETE FROM ordenes WHERE id = %s', (orden[0],))

            # Asignar la cita al usuario actual y marcarla como ocupada
            cursor.execute('''
                UPDATE citas
                SET estado = 'Ocupado', cliente_id = %s
                WHERE id = %s
            ''', (cliente_id, cita_id))

            conn.commit()
            conn.close()
            flash('Cita agendada exitosamente.')
            return redirect(url_for('user_menu'))
        else:
            conn.close()
            flash('La cita no está disponible. Por favor, seleccione otra cita.')
            return redirect(url_for('agendar_cita'))
    return redirect(url_for('login'))

@app.route('/ver_citas')
def ver_citas():
    if 'loggedin' in session and session.get('role') == 'user':
        conn = get_db_connection()
        cursor = conn.cursor()

        # Obtener las citas agendadas por el usuario actual
        cursor.execute('''
            SELECT c.fecha, c.cubiculo, d.nombre AS doctor
            FROM citas c
            JOIN doctores d ON c.doctor_id = d.id
            WHERE c.cliente_id = (
                SELECT id FROM usuarios WHERE username = %s
            )
        ''', (session['username'],))
        citas = cursor.fetchall()
        conn.close()

        # Renderizar la plantilla con las citas o un mensaje si no hay citas
        return render_template('ver_citas.html', citas=citas)
    return redirect(url_for('login'))

@app.route('/cancelar_citas', methods=['GET', 'POST'])
def cancelar_citas():
    if 'loggedin' in session and session.get('role') == 'user':
        conn = get_db_connection()
        cursor = conn.cursor()

        # Obtener las citas agendadas por el usuario actual
        cursor.execute('''
            SELECT c.id, c.fecha, c.cubiculo, d.nombre AS doctor
            FROM citas c
            JOIN doctores d ON c.doctor_id = d.id
            WHERE c.cliente_id = (
                SELECT id FROM usuarios WHERE username = %s
            )
        ''', (session['username'],))
        citas = cursor.fetchall()

        if request.method == 'POST':
            cita_id = request.form.get('cita_id')
            if cita_id:
                # Cancelar la cita seleccionada
                cursor.execute('''
                    UPDATE citas
                    SET estado = 'Disponible', cliente_id = NULL
                    WHERE id = %s
                ''', (cita_id,))
                conn.commit()
                flash('Cita cancelada exitosamente.')
                conn.close()
                return redirect(url_for('cancelar_citas'))

        conn.close()
        return render_template('cancelar_citas.html', citas=citas)
    return redirect(url_for('login'))

@app.route('/mi_perfil')
def mi_perfil():
    if 'loggedin' in session and session.get('role') == 'user':
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # Obtener la información del usuario actual desde la tabla clientes
            cursor.execute('''
                SELECT c.nombre, c.apellido, c.telefono, c.email, c.rh, c.sexo
                FROM usuarios u
                JOIN clientes c ON u.cliente_id = c.id
                WHERE u.username = %s
            ''', (session['username'],))
            perfil = cursor.fetchone()
        except Exception as e:
            conn.close()
            flash(f'Error al cargar el perfil: {str(e)}')
            return redirect(url_for('user_menu'))

        conn.close()

        if perfil:
            return render_template('mi_perfil.html', perfil=perfil)
        else:
            flash('No se pudo cargar la información del perfil.')
            return redirect(url_for('user_menu'))
    return redirect(url_for('login'))

@app.route('/mis_ordenes')
def mis_ordenes():
    if 'loggedin' in session and session.get('role') == 'user':
        conn = get_db_connection()
        cursor = conn.cursor()

        # Obtener las órdenes asignadas al usuario actual con el número de orden y la especialidad
        cursor.execute('''
            SELECT o.descripcion, 
                   CASE 
                       WHEN LEFT(o.descripcion, 2) = '01' THEN 'Cardiología'
                       WHEN LEFT(o.descripcion, 2) = '02' THEN 'Pediatría'
                       WHEN LEFT(o.descripcion, 2) = '03' THEN 'Ginecología'
                       WHEN LEFT(o.descripcion, 2) = '04' THEN 'Neurología'
                       WHEN LEFT(o.descripcion, 2) = '05' THEN 'Psiquiatría'
                       ELSE 'Especialidad Desconocida'
                   END AS especialidad
            FROM ordenes o
            JOIN usuarios u ON o.cliente_id = u.cliente_id
            WHERE u.username = %s
        ''', (session['username'],))
        ordenes = cursor.fetchall()
        conn.close()

        return render_template('mis_ordenes.html', ordenes=ordenes)
    return redirect(url_for('login'))

@app.route('/doctor_menu', methods=['GET', 'POST'])
def doctor_menu():
    if 'loggedin' in session and session.get('role') == 'doctor':
        if request.method == 'POST':
            option = request.form.get('option')
            if option == '1':  # Ver mi agenda
                return redirect(url_for('ver_agenda'))
            elif option == '2':  # Salir
                return redirect(url_for('logout'))
        return render_template('doctor_menu.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/ver_agenda')
def ver_agenda():
    if 'loggedin' in session and session.get('role') == 'doctor':
        conn = get_db_connection()
        cursor = conn.cursor()

        # Obtener la agenda del doctor actual con información del cliente si la cita está ocupada
        cursor.execute('''
            SELECT c.id AS cita_id, c.fecha, c.cubiculo, c.estado, 
                   cl.id AS cliente_id, cl.nombre AS cliente_nombre, cl.apellido AS cliente_apellido
            FROM citas c
            LEFT JOIN clientes cl ON c.cliente_id = cl.id
            WHERE c.doctor_id = (
                SELECT d.id FROM doctores d
                JOIN usuarios u ON u.username = d.nombre
                WHERE u.username = %s
            )
            ORDER BY c.fecha
        ''', (session['username'],))
        agenda = cursor.fetchall()
        conn.close()

        return render_template('ver_agenda.html', agenda=agenda)
    return redirect(url_for('login'))

@app.route('/asignar_orden/<int:cita_id>', methods=['GET', 'POST'])
def asignar_orden(cita_id):
    if 'loggedin' in session and session.get('role') == 'doctor':
        conn = get_db_connection()
        cursor = conn.cursor()

        # Obtener información del paciente asociado a la cita
        cursor.execute('''
            SELECT cl.id, cl.nombre, cl.apellido
            FROM citas c
            JOIN clientes cl ON c.cliente_id = cl.id
            WHERE c.id = %s
        ''', (cita_id,))
        paciente = cursor.fetchone()

        if request.method == 'POST':
            especialidad = request.form.get('especialidad')

            # Mapear especialidades a códigos
            especialidad_codigos = {
                'Cardiología': '01',
                'Pediatría': '02',
                'Ginecología': '03',
                'Neurología': '04',
                'Psiquiatría': '05'
            }
            codigo_especialidad = especialidad_codigos.get(especialidad, '00')

            # Generar un número único para la orden
            cursor.execute('SELECT COUNT(*) FROM ordenes')
            total_ordenes = cursor.fetchone()[0] + 1
            numero_orden = f"{codigo_especialidad}{str(total_ordenes).zfill(6)}"

            # Insertar una nueva orden para el cliente
            cursor.execute('''
                INSERT INTO ordenes (cliente_id, descripcion)
                VALUES (%s, %s)
            ''', (paciente[0], numero_orden))

            # Actualizar la cita: cambiar la fecha y el estado a 'Disponible'
            nueva_fecha = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('''
                UPDATE citas
                SET fecha = %s, estado = 'Disponible', cliente_id = NULL
                WHERE id = %s
            ''', (nueva_fecha, cita_id))

            conn.commit()
            conn.close()
            flash(f'Orden asignada exitosamente. Número de orden: {numero_orden}')
            return redirect(url_for('ver_agenda'))

        conn.close()
        return render_template('asignar_orden.html', paciente=paciente)
    return redirect(url_for('login'))

@app.route('/ver_citas_doctores')
def ver_citas_doctores():
    if 'loggedin' in session and session.get('role') == 'doctor':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.id AS cita_id, c.fecha, c.cubiculo, c.estado, d.nombre AS doctor
            FROM citas c
            JOIN doctores d ON c.doctor_id = d.id
            ORDER BY d.nombre, c.fecha
        ''')
        citas = cursor.fetchall()
        conn.close()
        return render_template('ver_citas_doctores.html', citas=citas)
    return redirect(url_for('login'))

@app.route('/eliminar_doctores_duplicados')
def eliminar_doctores_duplicados():
    if 'loggedin' in session and session.get('role') == 'doctor':
        conn = get_db_connection()
        cursor = conn.cursor()

        # Eliminar doctores duplicados manteniendo solo el primero
        cursor.execute('''
            DELETE FROM doctores
            WHERE id NOT IN (
                SELECT MIN(id)
                FROM doctores
                GROUP BY nombre, especialidad
            )
        ''')
        conn.commit()
        conn.close()
        flash('Datos duplicados eliminados correctamente.')
        return redirect(url_for('doctor_menu'))
    return redirect(url_for('login'))

@app.route('/eliminar_duplicados', methods=['GET'])
def eliminar_duplicados():
    if 'loggedin' in session and session.get('role') == 'doctor':
        conn = get_db_connection()
        cursor = conn.cursor()

        # Eliminar doctores duplicados manteniendo solo el primero
        cursor.execute('''
            DELETE FROM doctores
            WHERE id NOT IN (
                SELECT MIN(id)
                FROM doctores
                GROUP BY nombre, especialidad
            )
        ''')

        # Eliminar citas duplicadas manteniendo solo la primera
        cursor.execute('''
            DELETE FROM citas
            WHERE id NOT IN (
                SELECT MIN(id)
                FROM citas
                GROUP BY fecha, cubiculo, doctor_id
            )
        ''')

        conn.commit()
        conn.close()
        flash('Duplicados eliminados correctamente.')
        return redirect(url_for('doctor_menu'))
    return redirect(url_for('login'))

@app.route('/reset_doctores', methods=['GET'])
def reset_doctores():
    if 'loggedin' in session and session.get('role') == 'doctor':
        conn = get_db_connection()
        cursor = conn.cursor()

        # Borrar todos los registros de la tabla doctores
        cursor.execute('DELETE FROM doctores')

        # Reiniciar el contador de ID de la tabla doctores
        cursor.execute('ALTER TABLE doctores AUTO_INCREMENT = 1')

        conn.commit()
        conn.close()
        flash('Tabla doctores reiniciada correctamente.')
        return redirect(url_for('doctor_menu'))
    return redirect(url_for('login'))

@app.route('/reset_tablas', methods=['GET'])
def reset_tablas():
    if 'loggedin' in session and session.get('role') == 'doctor':
        conn = get_db_connection()
        cursor = conn.cursor()

        # Borrar todos los registros de la tabla citas
        cursor.execute('DELETE FROM citas')

        # Reiniciar el contador de ID de la tabla citas
        cursor.execute('ALTER TABLE citas AUTO_INCREMENT = 1')

        # Borrar todos los registros de la tabla doctores
        cursor.execute('DELETE FROM doctores')

        # Reiniciar el contador de ID de la tabla doctores
        cursor.execute('ALTER TABLE doctores AUTO_INCREMENT = 1')

        conn.commit()
        conn.close()
        flash('Tablas citas y doctores reiniciadas correctamente, IDs reseteados.')
        return redirect(url_for('doctor_menu'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('role', None)
    flash('Has cerrado sesión exitosamente.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)