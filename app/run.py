from app import site
import config
if __name__=="__main__":
    site.run(debug=config.DEBUG)#POST:FIXME:debuging to false in producrion.