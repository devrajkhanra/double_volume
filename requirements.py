import pkgutil

def list_installed_libraries():
    installed_libraries = [name for _, name, _ in pkgutil.iter_modules()]
    return installed_libraries

if __name__ == "__main__":
    libraries = list_installed_libraries()
    print("Installed Python libraries:")
    for library in libraries:
        print(library)
