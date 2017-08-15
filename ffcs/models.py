from py2neo import Graph, Node, Relationship
from datetime import datetime
from passlib.hash import bcrypt
import os
import uuid
url = os.environ.get('GRAPHENEDB_URL', 'http://localhost:7474')
username = os.environ.get('NEO4J_USERNAME')
password = os.environ.get('NEO4J_PASSWORD')
graph = Graph(url + '/db/data/', username=username, password=password)

class User:
	def __init__(self, username):
		self.username = username
	def find(self):
		user = graph.find_one('User', 'username', self.username)
		return user
	def register(self, password):
		if not self.find():
			user = Node('User', username=self.username, password=bcrypt.encrypt(password))
			graph.create(user)
			return True
		else:
			return False
	def verify_password(self, password):
		user = self.find()
		if(user):
			return bcrypt.verify(password, user['password'])
		else:
			return False
	#Add Course
	def add_course(self, course_name, course_code):
		user=self.find()
		course = Node(
			'Course',
			id=str(uuid.uuid4()),
			name=course_name,
			code=course_code,
			timestamp=timestamp(),
			date=date())
		rel = Relationship(user, 'REGISTERED', course)
		graph.create(rel)
	#Add pre-requisite course codes
	def add_preRequisite(self, course_code, pr_course_code):
		course = graph.find_one('Course', 'code', course_code)
		pr_course = graph.find_one('Course', 'code', pr_course_code)
		graph.merge(Relationship(pr_course, 'PREREQUISITE_OF', course))

#Generic Functions and queries

def fetch_all_courses():
	query = '''
	MATCH (n:Course) RETURN n.code as course_code, 
	n.name as course_name
	'''
	return graph.run(query)
def timestamp():
    epoch = datetime.utcfromtimestamp(0)
    now = datetime.now()
    delta = now - epoch
    return delta.total_seconds()

def date():
    return datetime.now().strftime('%Y-%m-%d')
