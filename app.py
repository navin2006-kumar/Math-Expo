from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)
#welcome page
@app.route('/')
def welcome():
    return render_template('welcome.html')
#home page
@app.route('/home')
def index():
    return render_template('home.html')
#matrix
@app.route('/matrix')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    operation = data.get('operation')
    matrix_a = np.array(data.get('matrixA', []))
    matrix_b = np.array(data.get('matrixB', [])) if 'matrixB' in data else None
    
    try:
        if operation == 'add':
            result = matrix_a + matrix_b
            return jsonify({'result': result.tolist()})
        elif operation == 'subtract':
            result = matrix_a - matrix_b
            return jsonify({'result': result.tolist()})
        elif operation == 'multiply':
            result = np.matmul(matrix_a, matrix_b)
            return jsonify({'result': result.tolist()})
        elif operation == 'determinant':
            result = np.linalg.det(matrix_a)
            return jsonify({'result': round(result, 4)})
        elif operation == 'inverse':
            result = np.linalg.inv(matrix_a)
            return jsonify({'result': result.tolist()})
        elif operation == 'transpose':
            result = np.transpose(matrix_a)
            return jsonify({'result': result.tolist()})
        elif operation == 'eigenvalues':
            result = np.linalg.eigvals(matrix_a)
            return jsonify({'result': result.tolist()})
        elif operation == 'rank':
            result = np.linalg.matrix_rank(matrix_a)
            return jsonify({'result': int(result)})
        else:
            return jsonify({'error': 'Invalid operation'})
    except Exception as e:
        return jsonify({'error': str(e)})
#calculator
@app.route('/sci')
def scientific_calculator():
    return render_template('calc.html')

#finance calculator
@app.route('/finan')
def f_cal():
    return render_template('fina.html')

@app.route('/calculate_emi', methods=['POST'])
def calculate_emi():
    try:
        principal = float(request.form['loan_amount'])
        rate = float(request.form['interest_rate'])
        tenure = float(request.form['loan_tenure'])
        
        # Convert tenure to months if in years
        if request.form['tenure_type'] == 'years':
            tenure *= 12
        
        monthly_rate = rate / 12 / 100
        emi = principal * monthly_rate * (1 + monthly_rate)**tenure / ((1 + monthly_rate)**tenure - 1)
        total_payment = emi * tenure
        total_interest = total_payment - principal
        
        return jsonify({
            'emi': round(emi, 2),
            'total_interest': round(total_interest, 2),
            'total_payment': round(total_payment, 2)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/calculate_fd', methods=['POST'])
def calculate_fd():
    try:
        principal = float(request.form['fd_amount'])
        rate = float(request.form['fd_rate'])
        tenure = float(request.form['fd_tenure'])
        interest_type = request.form['fd_interest_type']
        
        if request.form['fd_tenure_type'] == 'months':
            tenure /= 12
        
        if interest_type == 'simple':
            interest = principal * rate * tenure / 100
            maturity_amount = principal + interest
        else:  # compound
            n = 4  # quarterly compounding
            maturity_amount = principal * (1 + rate / (n * 100)) ** (n * tenure)
            interest = maturity_amount - principal
        
        return jsonify({
            'interest': round(interest, 2),
            'maturity_amount': round(maturity_amount, 2)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/calculate_ci', methods=['POST'])
def calculate_ci():
    try:
        principal = float(request.form['ci_amount'])
        rate = float(request.form['ci_rate'])
        tenure = float(request.form['ci_tenure'])
        n = float(request.form['compounding_frequency'])
        
        amount = principal * (1 + rate / (n * 100)) ** (n * tenure)
        interest = amount - principal
        
        return jsonify({
            'interest': round(interest, 2),
            'total_amount': round(amount, 2)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400
#graph
@app.route('/graph')
def grap():
    return render_template('graph.html')

@app.route('/calculate', methods=['POST'])
def g_calculate():
    data = request.get_json()
    try:
        # Here you could add server-side calculation if needed
        # For now we'll just validate the input
        return jsonify({'status': 'success', 'message': 'Function received'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})   
    
@app.route('/algebra')
def algebra():
    return render_template('algebra.html') 




if __name__ == '__main__':
    app.run(debug=True)