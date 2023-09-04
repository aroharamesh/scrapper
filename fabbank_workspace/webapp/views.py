
from flask import Flask, render_template, redirect, url_for,request,flash,jsonify, flash, send_from_directory,session




def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
        
    return update_wrapper(no_cache, view)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
@nocache
def dashboard():



    
    return render_template('dashboard.html')
