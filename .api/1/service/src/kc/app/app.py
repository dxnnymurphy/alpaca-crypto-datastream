from kc.app.datastream.pkg.application import Application, ApplicationFactory

def main():
    app: Application = ApplicationFactory.GetApplication(version="v1")
    app.Run()

if __name__ == '__main__':
    main()