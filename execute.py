import Polynomial_class
import Window

Window.app.title('I am fitting graphs!')
Window.app.mainloop()

try:
    fitted_polynomial = Window.app.get_polynomial()
    print(fitted_polynomial)
except TypeError:
    print("You haven't fitted any polynomial.")
