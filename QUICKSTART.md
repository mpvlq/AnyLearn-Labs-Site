# 🚀 Quick Start Guide

Get AnyLearn Labs running in 5 minutes!

## Windows Users

### Automated Setup (Recommended)

1. **Double-click `setup.bat`** - This will automatically:
   - Create a virtual environment
   - Install all dependencies
   - Set up the database
   - Create an admin account

2. **Double-click `run.bat`** to start the server

3. **Open your browser** to http://127.0.0.1:8000/

### Manual Setup

```cmd
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment
copy .env.example .env

# 5. Create database
python manage.py makemigrations
python manage.py migrate

# 6. Create admin user
python manage.py createsuperuser

# 7. (Optional) Add sample data
python manage.py populate_sample_data

# 8. Run server
python manage.py runserver
```

## Linux/Mac Users

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate it
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment
cp .env.example .env

# 5. Create database
python manage.py makemigrations
python manage.py migrate

# 6. Create admin user
python manage.py createsuperuser

# 7. (Optional) Add sample data
python manage.py populate_sample_data

# 8. Run server
python manage.py runserver
```

## Access Your Site

- **Main site**: http://127.0.0.1:8000/
- **Admin panel**: http://127.0.0.1:8000/admin/

## Adding Sample Data

To quickly populate your site with sample courses and blog posts:

```bash
python manage.py populate_sample_data
```

This creates:
- 3 sample courses (Statistics, Technical Writing, Machine Learning)
- 3 sample blog posts
- Admin user (username: `admin`, password: `admin123`)

## Next Steps

1. **Log in to the admin panel** to add your own courses and blog posts
2. **Customize the content** to match your brand
3. **Set up Stripe** (optional) for paid courses
4. **Configure email** (optional) for newsletters

## Troubleshooting

### "django-admin: command not found"
- Make sure your virtual environment is activated
- Try `python -m django` instead

### "Module not found" errors
- Run `pip install -r requirements.txt` again
- Make sure you're in the virtual environment

### Database errors
- Delete `db.sqlite3` and run migrations again:
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```

### Port already in use
- Use a different port: `python manage.py runserver 8001`

## Need Help?

Check the full [README.md](README.md) for detailed documentation!

---

**You're all set! Start building your learning platform! 🎓**
