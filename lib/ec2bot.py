#
# Telegram Bot EC2 
#

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging,boto3,MySQLdb,md5

class Ec2Bot:

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
    logger = logging.getLogger(__name__)
    region = None
    accesskey = None
    secretkey = None
    mysqlHost = None
    mysqlUser = None
    mysqlPassword = None
    mysqlDB = None

    def userCheck(self, email, password, id_instance):

        try:    
            con = MySQLdb.connect(host=self.mysqlHost, user=self.mysqlUser, passwd=self.mysqlPassword,db=self.mysqlDB)
            cursor = con.cursor()
            cursor.execute('SELECT count(1) FROM telegram_ec2.user U JOIN telegram_ec2.resource R ON R.id_user = U.id WHERE U.email = %s AND U.password = %s AND R.id_instance = %s ',[email,md5.new(password).hexdigest(),id_instance])
            if cursor.fetchone()[0] >= 1:
                return True 
            else:
                self.logger.info("This user cant do this action.")
                return False
        except:
            return False
            self.logger.info("Cant connect to database.")

    def connectBoto(self,option,region,accesskey,secretkey):

        if option == "resource":
            session = boto3.session.Session(aws_access_key_id=self.accesskey,aws_secret_access_key=self.secretkey,region_name=self.region)
            conn = session.resource("ec2")
        else:
            conn = boto3.client("ec2",aws_access_key_id=self.accesskey,aws_secret_access_key=self.secretkey,region_name=self.region)
        return conn

    def startBot(self,token,region,accesskey,secretkey,mysqlhost,mysqluser,mysqlpassword,mysqldb):

        self.region = region
        self.accesskey = accesskey
        self.secretkey = secretkey
        self.mysqlHost = mysqlhost
        self.mysqlUser = mysqluser
        self.mysqlPassword = mysqlpassword
        self.mysqlDB = mysqldb

        updater = Updater(token)

        dp = updater.dispatcher

        dp.add_handler(CommandHandler("start", self.startEc2, pass_args=True))
        dp.add_handler(CommandHandler("stop", self.stopEc2, pass_args=True))
        dp.add_handler(CommandHandler("help", self.help))
        dp.add_error_handler(self.error)

        updater.start_polling()
        updater.idle()

    def msg(self, update, opt, text):
        if opt == "warning":
            self.logger.warning(text)
        else:
            self.logger.info(text)
        return update.message.reply_text(text)

    def checkEc2Status(self,instanceID):

        try:
            result = self.connectBoto("resource",self.region,self.accesskey,self.secretkey)
            return result.Instance(instanceID).state['Name']
        except:
            return "checkError"

    def startEc2(self, bot, update, args):
        if len(args) < 3:
            self.ajuda(bot, update)
        else:
            try:
                if self.userCheck(args[0],args[1],args[2]):
                    if self.checkEc2Status(args[2]) == "stopped":
                        client = self.connectBoto("client",self.region,self.accesskey,self.secretkey)
                        client.start_instances(InstanceIds=[args[2]])
                        self.msg(update,"info","Starting instance "+args[2]+", wait 5 minutes after access.")
                    elif self.checkEc2Status(args[2]) == "checkError":
                        self.msg(update,"warning","Its not possible to start instance "+args[2]+".")
                    else:
                        self.msg(update,"info","Instance "+args[2]+" was started, please wait.")
                else:
                    self.msg(update,"warning","This user doesnt have permission to start instance.")
            except:
                self.msg(update,"warning","Its not possible to start instance "+args[2]+".")

    def stopEc2(self, bot, update, args):
        if len(args) < 3:
            self.ajuda(bot, update)
        else:
            try:
                if self.userCheck(args[0],args[1],args[2]):
                    if self.checkEc2Status(args[2]) == "running":
                        client = self.connectBoto("client",self.region,self.accesskey,self.secretkey)
                        client.stop_instances(InstanceIds=[args[2]])
                        self.msg(update,"info","Stopping instance "+args[2]+".")
                    elif self.checkEc2Status(args[2]) == "checkError":
                        self.msg(update,"warning","Its not possible to stop instance "+args[2]+".")
                    else:
                        self.msg(update,"info","Instance "+args[2]+" was stopped.")
                else:
                    self.msg(update,"warning","This user doesnt have permission to stop instance.")
            except:
                self.msg(update,"warning","Its not possible to stop instance "+args[2]+".")

    def help(self, bot, update):
        texto = 'Commands available:\n\n /start email password instanceID\n /stop email password instanceID'
        update.message.reply_text(texto)

    def error(self, bot, update, error):
        self.logger.warning('Update "%s" caused error "%s"', update, error)

