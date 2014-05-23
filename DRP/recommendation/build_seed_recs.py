#!/usr/local/bin/python

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
 # # Seed Recommendation Gen 'n Store  Worker Process  # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

#Necessary Imports:
import sys, os

#Grab the Django settings if they aren't already set.
django_dir = os.path.dirname(os.path.realpath(__file__)).split("DRP")[0]
django_path = "{}/DRP".format(django_dir)
if django_path not in sys.path:
  sys.path.append("{}/DRP".format(django_dir))

os.environ['DJANGO_SETTINGS_MODULE'] = 'DRP.settings'

from DRP.settings import BASE_DIR, LOG_DIR
import DRP.models
import django.db

from DRP.emailFunctions import email_user, email_admins
from DRP.retrievalFunctions import *
from DRP.database_construction import *
from DRP.compoundGuideFunctions import 
from DRP.recommendation.seed_rec import constructRecsFromSeed
from DRP.logPrinting import print_error, print_log
from DRP.cacheFunctions import *

#An independent worker process for generating and storing seeds in the database.
def seed_rec_worker(lab_id, seed_id, user_id):
  print_log("Seed Rec: {} {} {}".format(lab_id, seed_id, user_id))

  try:
    #Restart the database connection for this new process.
    django.db.close_connection()

    #Get the objects from the database (assuming validation has already passed).
    seed = Data.objects.get(id=seed_id)
    lab_group = Lab_Group.objects.get(id=lab_id)
    user = User.objects.get(id=user_id)
  except Exception as e:
    print_error("Can't load entries: {} {} {}".format(lab_id, seed_id, user_id))

  try:
    #Actually create new recommendations...
    try:
      recList = constructRecsFromSeed(seed_id)
    except Exception as e:
      raise Exception("constructRecsFromSeed failed: {}".format(e))

    #Translate any compounds in the recList to abbrevs.
    recList = translate_reactants(lab_group, recList)

    #And store them in the database.
    store_new_Recommendation_list(lab_group, recList, seed_source=seed)

    email_body = "The recommendations based on Reaction \"{}\" have finished!".format(seed.ref)
    email_user(user, "Seed Recommendations Ready", email_body)

  except Exception as e:
    #Log any errors that might have occurred.
    print_error("{} {} {}".format(lab_id, seed_id, user_id), details=e)

    #Email the user that this batch of recommendations failed.
    email_body = "We're very sorry, but the recommendations based on Reaction \"{}\" could not be created! Please let us know so that we can fix this!".format(seed.ref)
    email_user(user, "Seed Recommendations Failed!", email_body)

    #Also email the admins so that they can address the problem.
    email_body = ("Seed Recommendation Failed... (check .../DRP/logs/ for more)\n"+
            "Seed-Rec Worker: {} {} {}\n".format(lab_id, seed_id, user_id)+
            "__________\n"+
            "Error: {}".format(e)+
            "__________\n")
    email_admins("Fatal Failure: Seed Recs Failed!", email_body)

  finally: #In the case that emailing fails, always uncache the process.
    remove_seed_rec_worker_from_cache(lab_group, seed.ref)


if __name__ == "__main__":
  if len(sys.argv) != 4:
    print "You probably want to let the UI handle this..."
    print "python ./this_script.py lab_id seed_data_id user_id"
  else:
    seed_rec_worker(sys.argv[1], sys.argv[2], sys.argv[3])
    

