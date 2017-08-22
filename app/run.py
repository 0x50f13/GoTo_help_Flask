from app import site
import app.views
import config
if __name__=="__main__":
    site.run(debug=config.DEBUG)#POST:FIXME:debuging to false in producrion.