from flask import (current_app,
                   flash,
                   redirect,
                   render_template,
                   request,
                   url_for)

from flask.ext.login import (login_user,
                             logout_user,
                             login_required,
                             current_user)

from . import admin
from .. import db
from ..decorators import admin_required, permission_required
from .forms import (AddTeacherForm,
                    ExcelUploadForm,
                    EditTeacherForm,
                    AddWorkPeriodForm,
                    EditWorkPeriodForm)
from ..models import User, WorkPeriod
from sqlalchemy import desc


@admin.route('/', methods=['GET', 'POST'])
@login_required
@admin_required
def index():
    """Main route for admin user interface.

    Administrator permissions is required to
    grant acess to this page.
    """
    return render_template('admin/admin.html')


@admin.route('/teachers', methods=['GET', 'POST'])
@login_required
@admin_required
def teachers():
    teachers = User.query.filter_by(password_hash=None).order_by(User.first_name)
    return render_template('admin/teachers.html', teachers=teachers)


@admin.route('/teachers/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_teacher():
    form = AddTeacherForm()

    if form.validate_on_submit():
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('admin.teachers'))

    return render_template('admin/add.html', form=form, form_name='lärare')


@admin.route('/teachers/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_teacher(id):
    user = User.query.filter_by(id=id).first()
    form = EditTeacherForm(obj=user)

    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for('admin.teachers'))

    return render_template('admin/edit.html', form=form, form_name='lärare')


@admin.route('/teachers/upload', methods=['GET', 'POST'])
@login_required
@admin_required
def upload_teachers():
    form = ExcelUploadForm()

    if form.validate_on_submit():
        pass

    return render_template('admin/upload.html', form=form)


@admin.route('/work-periods/', methods=['GET', 'POST'])
@login_required
@admin_required
def work_periods():
    work_periods = WorkPeriod.query.order_by(desc(WorkPeriod.start))
    # TODO - fix date-datatype and populate db
    return render_template('admin/work_periods.html', work_periods=work_periods)


@admin.route('/work-periods/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_work_period():
    form = AddWorkPeriodForm()

    if form.validate_on_submit():
        work_period = WorkPeriod(start=form.start.data, end=form.end.data)
        db.session.add(work_period)
        db.session.commit()
        return redirect(url_for('admin.work_periods'))

    return render_template('admin/add.html', form=form, form_name='arbetsperiod')


@admin.route('/work-periods/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_work_period(id):
    work_period = WorkPeriod.query.filter_by(id=id).first()
    form = EditWorkPeriodForm(obj=work_period)

    if form.validate_on_submit():
        form.populate_obj(work_period)
        db.session.commit()
        return redirect(url_for('admin.work_periods'))

    return render_template('admin/edit.html', form=form, form_name='arbetsperiod')
