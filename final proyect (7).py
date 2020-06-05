import random

class Account:
    def __init__(self, username, password):
        self.username = username
        self.password = password             

class Course: 
    def __init__(self, name, code, unit):
        self._courseName = name
        self._courseCode = code
        self._courseUnit = unit

    #This method returns the name of the course
    def getCourseName(self):
        return self._courseName
    
    #This method is used to get the code of the course
    def getCourseCode(self):
        return self._courseCode

    #This method gets the unit of the course, which is the weight of the course
    def getCourseUnit(self):
        return self._courseUnit


class TakenCourse(Course):
    def __init__(self, collegeCourse, semester, grade=0):
        name = collegeCourse.getCourseName()
        code = collegeCourse.getCourseCode()
        unit = collegeCourse.getCourseUnit()
        super().__init__(name, code, unit)

        self._semester = semester
        self._grade = grade

        
    def printCourse(self):
        print("Course Name: %s || Course Code: %s || Course Unit %d " % (self._courseName, self._courseCode, self._courseUnit))
        self._semester.printSemester()
        print("Grade %d \n" % (self._grade))
    
    def getCurrentSemester(self):
        currentSemester = self._semester.iscurrentSemester()
        return currentSemester
    
    def getGrade(self):
        return self._grade
    
    def getUnit(self):
        return super().getCourseUnit()

    def getSemester(self):
        return self._semester
    
class CollegeCourse(Course):
    def __init__(self, name, code, unit):
        super().__init__(name, code, unit)
        self._courseUnit = unit

    def printCourse(self):
        print("Course Name: %s | Course Code: %s | Course Unit %d \n" % (self._courseName, self._courseCode, self._courseUnit))

    #They return the course name saved in the parent class
    def getCourseName(self):
        return super().getCourseName()
    
    #They return the course code saved in the parent class
    def getCourseCode(self):
        return super().getCourseCode()
   
    #They return the course unit saved in the parent class
    def getCourseUnit(self):
        return super().getCourseUnit()

class Student:
    def __init__(self, studentProfile, account, manager, admissionYear=2018):
        self._admissionYear = admissionYear
        self._admissionSemester = 1  # Suppose each student starts in semester 1 of the admission year
        self._generalTranscript = GeneralTranscript()
        self._semesterTranscript = CurrentSemesterTranscript()
        self._studentProfile = studentProfile
        self._manager = manager #This is only for the enrollmentCertificate. It displays the name of the manager
        self._account = account #The account contains the Username and password of each student
        
    #It returns the data saved in studentProfile
    def getStudentProfile(self):
        return self._studentProfile
    
    def getAdmissionYear(self):
        return self._admissionYear


    def registerCourse(self, collegeCourse, semester, grade=0):

        courseRegistrationYear = semester.getYear()
        courseRegistrationSemester = semester.getSemesterNo()

        course = TakenCourse(collegeCourse, semester, grade)

        if semester.isCurrentSemester():
            self._semesterTranscript.addCourse(course)
            self._generalTranscript.addCourse(course)
        else:
            self._generalTranscript.addCourse(course)

    def getGTranscript(self):
        return self._generalTranscript

    def getSTranscript(self):
        return self._semesterTranscript
    
    #This is mainly to display the correct greeting for students in the enrollmentCertificate
    def getTitle(self):
        gender = self._studentProfile.gender
        title = ''
        if gender == 'M':
            return 'Mr.'
        elif gender == 'F':
            return 'Ms.'
        else:
            return 'Mr./Ms.'        

    #This basically gets the data of the student and prints a certificate. The data collects the profiles of the student and the courses. Also prints the manager name
    def printEnrolmentCertificate(self):        
        title = self.getTitle()
        countCoursesTaken = self._generalTranscript.getCountCourses()
        print()
        print("Dear Sir/Madam,")
        print(f'This is to certify that {title} {self._studentProfile.firstName + " " + self._studentProfile.lastName} with student id {self._studentProfile.studentId} is a student at semester {self._admissionSemester} at CICCC.')
        print(f'He was admitted to our college in {self._admissionYear} and has taken {countCoursesTaken} course(s) so far. Currently he resides at ')
        print(f'{self._studentProfile.address}, {self._studentProfile.country}.')
        print('If you have any question, please do not hesitate to contact us.')
        print('Thanks,')
        print(f'[Manager: {self._manager.firstName + " " + self._manager.lastName} ]')        
    
    #It prints the courses that the student has taken so far. 
    def printMyCourses(self):        
        title = self.getTitle()
        print()
        print("Hi", title, self._studentProfile.firstName + " " + self._studentProfile.lastName)
        print("You have taken the following courses so far: ")
        
        counter = 1
        for course in self._generalTranscript.getCourses():
            semester = ""
            if course.getSemester().isCurrentSemester() == True:
                semester = " [Current Semester]"            
            print (f'{counter}) {course.getCourseCode()}: {course.getCourseName()} {semester}')
            counter = counter + 1
    
    #The method get the gpa of the student for each course taken and returns the overallGpa      
    def getOverallGpa(self):
        gpa = 0
        totalUnit = 0
        finalGpa = 0
        for course in self._generalTranscript.getCourses():

            gpa = gpa + (course.getGrade() * course.getUnit())          
            totalUnit = totalUnit + course.getUnit()   

        if totalUnit > 0:
            finalGpa = gpa/totalUnit
        return round(finalGpa,2)

    #The method returns the gpa of the current semester for the courses taken during the semester.
    def getCurrentGpa(self):
        gpa = 0
        divGpa = 0
        totalUnit = 0
        for course in self._semesterTranscript.getCurrentCourses():
            gpa = gpa + (course.getGrade() * course.getUnit()) 
            totalUnit += course.getUnit()
        if totalUnit > 0:
            divGpa = gpa / totalUnit

        return round(divGpa,2)    
    
    #It displays a general information about the student regarding to the student's courses and gpa.
    def printMyTranscript(self):
        title = self.getTitle()
        print()
        print("Hi", title, self._studentProfile.firstName + " " + self._studentProfile.lastName)
        print("Here is your general transcript:")
        
        counter = 1
        for course in self._generalTranscript.getCourses():
            semester = ""
            if course.getSemester().isCurrentSemester() == True:
                semester = " [Current Semester]"            
            print (f'{counter}) {course.getCourseCode()}: {course.getCourseName()}: {course.getGrade()} {semester}')
            counter = counter + 1                                     
        print ("YOUR GPA IS:", self.getOverallGpa()) 

        print()
        print("Here is your current semester transcript:")
        
        counter = 1
        for course in self._semesterTranscript.getCurrentCourses():
            semester = ""
            if course.getSemester().isCurrentSemester() == True:
                semester = " [Current Semester]"            
            print (f'{counter}) {course.getCourseCode()}: {course.getCourseName()}: {course.getGrade()} {semester}')
            counter = counter + 1              
        print ("YOUR Current Semester GPA IS:", self.getCurrentGpa())         
    
    #This method print the overall and the current gpa    
    def printGpa(self):
        title = self.getTitle()
        print(f'Hi {title}{self._studentProfile.firstName} {self._studentProfile.lastName},')
        print (f'Your overall GPA is  {self.getOverallGpa()}')                               
        print (f"Your current semester GPA is {self.getCurrentGpa()}")
        
    #It prints a list of the courses taken so far
    def getCoursesTaken(self):
        Coursestaken = {}
        counter = 1
        course = ""
        for course in self._generalTranscript.getCourses():
            semester = ""
            if course.getSemester().isCurrentSemester() == True:
                semester = " [Current Semester]"         
            course = {course.getCourseCode() : course.getCourseName() }
            Coursestaken.update(course)
            
        return Coursestaken
    
    #This method prints the data of the student. (Name, courses taken, gender, etc)
    def getShowProfile(self):
        title = self.getTitle()
        genderV = ''
        overallGpa = self.getOverallGpa()
        coursesTaken = self.getCoursesTaken()
        print (f'Name: {title} {self._studentProfile.firstName} {self._studentProfile.lastName}')
        print (f'StudentID: {self._studentProfile.studentId}')
        if self._studentProfile.gender == 'M':
            genderV = 'Male'
        elif self._studentProfile.gender == 'F':
            genderV = 'Female'
        elif self._studentProfile.gender == 'O':
            genderV = 'Other'
        else:
            genderV = 'Gender not specified'
            
        print (f'Gender: {genderV}')
        
        print (f'Address: {self._studentProfile.address}')
        print(f'Country of Origin: {self._studentProfile.country}')
        print (f'Age: {self._studentProfile.age}')
        print (f'Year of Admission: {self._admissionYear}')
        print (f'Overall GPA: {overallGpa}')
        print (f'Courses Taken So far:', coursesTaken)      
    
    
    #This list prints the courses that the student has taken so far
    def getCourses(self, listCourses):
        coursesTaken = {}        
        
        for taken in self._generalTranscript.getAllTakenCourses():
            coursesTaken[taken.getCourseCode()] = taken.getSemester().getSemesterNo()
            
        counter = 1
        for course in listCourses:
            takenMessage = "[Not Taken]"
            if course.getCourseCode() in coursesTaken.keys():
                takenMessage = "[Taken at semester " + str(coursesTaken[course.getCourseCode()]) + "]"
                
            print (f'{counter}) {course.getCourseCode()} {course.getCourseName()} {course.getCourseUnit()} units {takenMessage}')
            counter = counter + 1
        
    #The method returns the first name, last name and the student id.
    def getStudentInfo(self):
        return self._studentProfile.firstName + ' ' + self._studentProfile.lastName + ': ' + str(self._studentProfile.studentId)
    
    #This student returns the student's gpa and it compares it with the other students.
    def getMyRankingGpa(self, listGpa):
        title = self.getTitle()
        listGpa.sort(reverse=True)
        myGpa = self.getOverallGpa()
        ranked = 0
        
        for i in range(0, len(listGpa)):
            if listGpa[i] < myGpa:
                ranked = i + 1
                break
        if ranked == 0:
            ranked = len(listGpa) + 1
            
        print(f'Hi {title} {self._studentProfile.firstName} {self._studentProfile.lastName}')
        print(f'Your overall GPA is {myGpa} and therefore your rank is {ranked}.')
    
class StudentProfile:
    def __init__(self, firstName, lastName, gender, country, age, studentId, address):
        self.firstName = firstName
        self.lastName = lastName
        self.gender = gender
        self.country = country
        self.age = age
        self.studentId = studentId #This saves the student, a random 8 number
        self.address = address #This saves the city where the student lives

class Transcript:
    def __init__(self):
        self._allTakenCourses = []
        self._currentTakenCourses = [] #List of the coursestaken the current semester


    def addCourse(self, takenCourse):
        self._allTakenCourses.append(takenCourse)
        
        if takenCourse._semester.isCurrentSemester():
            self._currentTakenCourses.append(takenCourse)        

    def printTranscript(self):
        for c in self._allTakenCourses:
            c.printCourse()
    
    #This method returns the courses taken so far
    def getAllTakenCourses(self):
        return self._allTakenCourses
    
    #This method returns the courses taken during the current semester
    def getCurrentTakenCourses(self):
        return self._currentTakenCourses
        

class GeneralTranscript(Transcript):
    def __init__(self):
        super().__init__()
    
    #It counts the courses taken so far in the parent class(Transcript) and return it
    def getCountCourses(self):
        count = 0
        for course in super().getAllTakenCourses():
            count = count + 1
        
        return count
    
    #It returns the courses taken for the student in the parent class(Transcript).
    def getCourses(self):
        return super().getAllTakenCourses()      
           
    
class CurrentSemesterTranscript(Transcript):
    def __init__(self):
        super().__init__()
     
     #The method gets the courses taken during the semester 
    def getCurrentCourses(self):
        return super().getCurrentTakenCourses()


#It is class for the object manager, mainly used for the enrollmentcertificate
class Manager:
    def __init__(self, firstName, lastName, title):
        self.firstName = firstName
        self.lastName = lastName
        self.title = title        

class Semester:
    def __init__(self, semesterNo, year):
        self._semesterNo = semesterNo
        self._year = year
        self._setIfCurrentSemester()

    def getYear(self):
        return self._year

    def getSemesterNo(self):
        return self._semesterNo

    # checks whether the semester object is representing current semester or not. Suppose, current semester is year = 2019, semester = 2
    def _setIfCurrentSemester(self):
        currentSemester = 2
        currentYear = 2019

        if (self._semesterNo == currentSemester) and (self._year == currentYear):
            self._isCurrentSemester = True
        else:
            self._isCurrentSemester = False

    def isCurrentSemester(self):
        return self._isCurrentSemester        

    def printSemester(self):
        print("Year: %d Semester%d isCurrent %d" % (self._year, self._semesterNo, self._isCurrentSemester))

#it show some reports of general students.
class Classroom:
    #This method returns a list of the gpa of all students. And sort them high to low    
    def getListStudentGpa(self, portal):
        listGpa=[]
        for st in portal.getRegisteredStudents():
            listGpa.append({'studentId':st.getStudentProfile().studentId, 
                            'studentName':st.getStudentProfile().firstName + ' ' + st.getStudentProfile().lastName,
                            'gpa' : st.getOverallGpa()})
        newList = sorted(listGpa, key = lambda i: i['gpa'], reverse=True)
        counter = 1
        for st in newList:
            print(f'{counter}) {st["studentName"]}: {st["studentId"]} gpa: {st["gpa"]}')
            counter += 1    
    
    #This returns a list of all student sorted by name
    def getListStudents(self, portal):
        listStudentNames=[]
        for st in portal.getRegisteredStudents():
            name = st.getStudentProfile().firstName + ' ' + st.getStudentProfile().lastName
            listStudentNames.append(name)                                  
        newList = sorted(listStudentNames)
        counter = 1
        for st in newList:
            print(f'{counter}) {st}')
            counter += 1            
    
    #This returns a list of student by gender. For a specific gender.
    def getListStudentsByGender(self, portal, gender):
        listStudentNames=[]
        for st in portal.getRegisteredStudents():
            if st.getStudentProfile().gender == gender:
                name = st.getStudentProfile().firstName + ' ' + st.getStudentProfile().lastName
                listStudentNames.append(name)                                  
        newList = sorted(listStudentNames)
        counter = 1
        for st in newList:
            print(f'{counter}) {st}')
            counter += 1                           
        
    #This returns 3 dicts of student, each dict contains the gpa of students 
    def getBiggestGpaByGender(self, portal):
        male={}
        female={}
        other={}
        biggestMaleGpa = -1
        biggestFemaleGpa = -1
        biggestOtherGpa = -1
        
        for st in portal.getRegisteredStudents():
            gpa = st.getOverallGpa()
            if st.getStudentProfile().gender == "M":
                if biggestMaleGpa <= gpa:
                    male['studentId']= st.getStudentProfile().studentId
                    male['studentName']= st.getStudentProfile().firstName + ' ' + st.getStudentProfile().lastName
                    male['gender'] = st.getStudentProfile().gender
                    male['gpa'] = gpa
                    biggestMaleGpa = gpa
            elif st.getStudentProfile().gender == "F":
                if biggestFemaleGpa <= gpa:
                    female['studentId']= st.getStudentProfile().studentId
                    female['studentName']= st.getStudentProfile().firstName + ' ' + st.getStudentProfile().lastName
                    female['gender'] = st.getStudentProfile().gender
                    female['gpa'] = gpa
                    biggestFemaleGpa = gpa
            else:
                if biggestOtherGpa <= gpa:
                    other['studentId']= st.getStudentProfile().studentId
                    other['studentName']= st.getStudentProfile().firstName + ' ' + st.getStudentProfile().lastName
                    other['gender'] = st.getStudentProfile().gender
                    other['gpa'] = gpa
                    biggestOtherGpa = gpa                            
        if biggestMaleGpa > -1:            
            print("Biggest male Gpa")
            print(f'{male["studentName"]}: {male["studentId"]} gpa: {male["gpa"]}')
        if biggestFemaleGpa > -1:
            print("Biggest female Gpa")
            print(f'{female["studentName"]}: {female["studentId"]} gpa: {female["gpa"]}')
        if biggestOtherGpa > -1:
            print("Biggest other Gpa")
            print(f'{other["studentName"]}: {other["studentId"]} gpa: {other["gpa"]}')
            
#This class is for the interface menu, 
class Menu:        
        def __init__(self):
            self._prinicipalMenu = []
            self._bonusMenu = []
            
        #This method is for creating each option of the principal menu
        def registerPpalMenu(self, menu):
            self._prinicipalMenu.append(menu)
        
        #This creates the bonus menu    
        def registerBonusMenu(self, menu):
            self._bonusMenu.append(menu)
        
                       
            
class Portal:
    # _currentSemester = Semester(2019, 2)  # Static/class property. Suppose the current semester is second semester 2019
    def __init__(self):
        self._collegeCourses = []
        self._registeredStudents = []

    # use this method to register a student
    def registerStudent(self, student):
        self._registeredStudents.append(student)

    def addCourse(self, collegeCourse):
        self._collegeCourses.append(collegeCourse)
    # class this method to add some random courses to a student - You don't need to understand how this method works. Just call it and it will add some courses
    # to the student and to different semesters

    def addRandomCoursesToStudent(self, student):
        for course in self._collegeCourses:
            rand = random.uniform(0, 1)
            admissionYear = student.getAdmissionYear()
            currentSemester = Portal.getCurrentSemester()

            if currentSemester.getYear() == admissionYear:
                numberOfSemesterBetweenCurrentSemesterAndAdmission = currentSemester.getSemesterNo()
            else:
                numberOfSemesterBetweenCurrentSemesterAndAdmission = 2 * (currentSemester.getYear() - admissionYear) + currentSemester.getSemesterNo()

            randomSemster = random.randint(1, numberOfSemesterBetweenCurrentSemesterAndAdmission - 1)

            year = randomSemster // 2
            semesterNo = (randomSemster % 2) + 1
            semester = Semester(semesterNo, student.getAdmissionYear() + year)

            randomGrade = random.randint(30, 100)

            if rand <= .5:
                student.registerCourse(course, semester, randomGrade)

    # static/class method
    def getCurrentSemester():
        currentSemester = Semester(2, 2019)  # Static/class property. Suppose the current semester is second semester 2019
        return currentSemester

    #this returns a list of students.
    def getRegisteredStudents(self):
        return self._registeredStudents
    
    #This returns a list of courses. 
    def getRegisteredCourses(self):
        return self._collegeCourses

class PortalManager:
    def __init__(self):
        self._portal = Portal()
        self._menu = Menu()  # This creates the instance menu
        self._classroom = Classroom()
        self._manager = Manager("Peter", "Jackson", "Mr") #This assigns the manager data
    
    def getPortal(self):
        return self._portal
        
    #This method registers a new student.   
    def registerNewStudent(self, firstName, lastName, gender, country, address, admisionYear, age, username, password):
        # create a student
        sampleStudentProfile = StudentProfile(firstName, lastName, gender, country, age, random.randint(1000000, 99999999), address)
        sampleAccount = Account(username,password)
        sampleStudent1 = Student(sampleStudentProfile, sampleAccount, self._manager, admisionYear)

        # register the student
        self._portal.registerStudent(sampleStudent1)

        # add some random courses with grades to the student
        self._portal.addRandomCoursesToStudent(sampleStudent1)

        #sampleStudent1.getGTranscript().printTranscript()  
        
        return sampleStudent1    

    def createATestPortal(self):
       
        # create all courses offered
        self._createAllCollegeCourses()
        # self._portal.printAllCollegeCourses()
        
        self.registerNewStudent("Peter", "Sand", "M", "Irland", "Dublin", 2017, 30, "Student1", "111111")
        self.registerNewStudent("Sheila", "Rogers", "F", "India", "New Delhi", 2017, 30, "Student2", "222222")
        self.registerNewStudent("Edward", "Richards", "M", "China", "Pekin", 2017, 30, "Student3", "333333")
        self.registerNewStudent("Souzan", "Robson", "F", "India", "Noida", 2017, 30, "Student4", "444444")
        self.registerNewStudent("Jeff", "Cooper", "M", "England", "New Hampshire", 2017, 30, "Student5", "555555")   

    # create menus
    def _createAllMenus(self):
        #Create Bonus Menu
        self._menu.registerBonusMenu("--[1] Print the list of all students based on their GPA (Ascendingly)")
        self._menu.registerBonusMenu("--[2] Print the list of names of all students alphabetically")
        self._menu.registerBonusMenu("--[3] Print the list of all Male students")
        self._menu.registerBonusMenu("--[4] Print the list of all Female students")
        self._menu.registerBonusMenu("--[5] List of top (highest GPA) male and female students")
        self._menu.registerBonusMenu("--[6] Back to the previous menu")
        
        #Create Principal Menu        
        self._menu.registerPpalMenu("--[1] Print my enrolment certificate")
        self._menu.registerPpalMenu("--[2] Print my courses")
        self._menu.registerPpalMenu("--[3] Print my transcript")
        self._menu.registerPpalMenu("--[4] Print my GPA")
        self._menu.registerPpalMenu("--[5] Print my ranking among all students in the college")
        self._menu.registerPpalMenu("--[6] List all available courses")
        self._menu.registerPpalMenu("--[7] List all students")
        self._menu.registerPpalMenu("--[8] Show My Profile")
        self._menu.registerPpalMenu("--[9] Logout")
        self._menu.registerPpalMenu("--[10] Exit")
        self._menu.registerPpalMenu("--[11] Bonus")
        
    # create college courses
    def _createAllCollegeCourses(self):
        python = CollegeCourse("Python", "CSCI101", 3)
        objectOrientedProgramming = CollegeCourse("Python", "CSCI102", 2)
        problemSolving = CollegeCourse("Problem Solving", "CSCI201", 1)
        projectManagement = CollegeCourse("Project Management", "CSCI202", 3)
        javaProgramming = CollegeCourse("Java Programming", "CSCI301", 3)
        webDevelopment = CollegeCourse("Web Development", "CSCI302", 2)
        androidProgramming = CollegeCourse("Android Programming", "CSCI401", 2)
        iOSApplication = CollegeCourse("iOS Application", "CSCI402", 3)

        self._portal.addCourse(python)
        self._portal.addCourse(objectOrientedProgramming)
        self._portal.addCourse(problemSolving)
        self._portal.addCourse(projectManagement)
        self._portal.addCourse(javaProgramming)
        self._portal.addCourse(webDevelopment)
        self._portal.addCourse(androidProgramming)
        self._portal.addCourse(iOSApplication)
    
    #This is where the principal menu gets displayed.     
    def startPpalMenu(self, student):
        flag = True;
        while flag == True:
            print("************************************************************")
            print("Select from the options:")
            print("************************************************************")
            for menuPpal in self._menu._prinicipalMenu:
                print(menuPpal)
            print()
            print("************************************************************")
            value = input("Enter the number corresponding to each item to proceed: ")
            while not value.isnumeric() or value == "":
                value = input("Enter the number corresponding to each item to proceed: ")
            value = int(value)
            while (value < 1 or value  > 11):
                print("Menu Not implemented")
                value = int(input("Enter the number corresponding to each item to proceed: "))
            if value == 1:
                student.printEnrolmentCertificate()
                input("Press ENTER to continue...")
            elif value == 2:
                student.printMyCourses()
                input("Press ENTER to continue...")
            elif value == 3:
                student.printMyTranscript()
                input("Press ENTER to continue...")
            elif value == 4:
                student.printGpa()
                input("Press ENTER to continue...")
            elif value == 5:
                listGpa=[]
                for st in self._portal._registeredStudents:
                    if st != student:
                        listGpa.append(st.getOverallGpa())
                student.getMyRankingGpa(listGpa)
                input("Press ENTER to continue...")                
            elif value ==6:
                student.getCourses(self._portal._collegeCourses)
                input("Press ENTER to continue...")
            elif value == 7:
                counter = 1
                print(f'There are {len(self._portal._registeredStudents)} students in CICCC College as following:')
                for st in self._portal._registeredStudents:
                    print(f'{counter}) {st.getStudentInfo()}')
                    counter += 1
                input("Press ENTER to continue...")
            elif value == 8:
                student.getShowProfile()
                input("Press ENTER to continue...")
            elif value == 9:
                flag = False
                self.login()
            elif value == 10:
                input("Application terminated.  Press ENTER to exit")
                exit()
            elif value == 11:
                self.startBonusMenu(student)                
            else:
                print("Menu Not implemented")
                input("Press ENTER to continue...")
    
    #The bonus menu gets displayed                        
    def startBonusMenu(self, student):        
        flag = True;
        while flag == True:        
            print("************************************************************")
            print("**Welcome to the extra features of the application**")
            print("************************************************************")
            for menuBonus in self._menu._bonusMenu:
                print(menuBonus)
            print()
            print("************************************************************")
            value = input("Enter the number corresponding to each item to proceed: ")
            while not value.isnumeric() or value == "":
                value = input("Enter the number corresponding to each item to proceed: ")
            value = int(value)
            while (value < 1 or value  > 11):
                print("Menu Not implemented")
                value = int(input("Enter the number corresponding to each item to proceed: "))    
            if value == 1:
                self._classroom.getListStudentGpa(self.getPortal())
                input("Press ENTER to continue...")                                 
            elif value == 2:
                self._classroom.getListStudents(self.getPortal())
                input("Press ENTER to continue...")               
            elif value == 3:
                self._classroom.getListStudentsByGender(self.getPortal(), 'M')
                input("Press ENTER to continue...")            
            elif value == 4:
                self._classroom.getListStudentsByGender(self.getPortal(), 'F')                
                input("Press ENTER to continue...")                
            elif value == 5:
                self._classroom.getBiggestGpaByGender(self.getPortal())                             
                input("Press ENTER to continue...")                     
                
            elif value == 6:
                flag = False                                               
            else:
                print("Menu Not implemented")
                input("Press ENTER to continue...")            
    #This method is has the code for registering the studnt. it ask the data of the new user and save it.   
    def register(self):
        print("************************************************************")
        print("Welcome to CICCC College: Please Register")
        print("************************************************************")
        
        firstName = input("Please enter your first: name: ").strip()
        lastName = input("Please enter your last name: ").strip()
        gender = input("Please enter your gender [M/F/O]: ").upper()
        while gender not in("M","F","O") :
            gender = input("Please re-enter your gender only accept [M/F/O]: ").upper()            
        country = input("Please enter you country of origin: ")
        address = input("Please enter your address: ")
        admisionYear = input("Please enter the year of admision: ") 
        while not admisionYear.isnumeric():
            admisionYear = input("Please enter the year of admision (only accept numbers): ") 
        admisionYear = int(admisionYear)
        print()
        age = input("Please enter your age: ")
        while not age.isnumeric():
            age = input("Please enter your age (only accept numbers): ")
        age = int(age)
        print()
        username = input("Please enter a username [At least 6 characters]: ")
        while (len(username) < 6):
            username = input("Please re-enter a username [You must enter at least 6 characters]: ")        
            
        password = input("Please enter a password [At least 6 characters with at least one digit]: ")                 
        while len(password) < 6 or (not any(element.isdigit() for element in password)):            
            password = input("Please enter a password [At least 6 characters with at least one digit]: ")
 
       
        student = self.registerNewStudent(firstName, lastName, gender, country, address, admisionYear, age, username, password)
        print('Thanks, your account and profile has been created successfully. Welcome Aboard',firstName, lastName)
        input('Press enter to continue...')
        return student
     
    #This displays the instance login. Used to access to the menu   
    def login(self):
        print('************************************************************')
        print('Please enter your account to login:')
        print('************************************************************')
        print('----------------')
        print('Not registered yet? Type "Register" and press enter to start the registration process!')
        print()
        username = input("Username: ")        
        if username.upper() == "REGISTER":            
            student = self.register()
            self.startPpalMenu(student)
        else:
            password = input("enter the password: ")
            exists = False
            students = self._portal.getRegisteredStudents()        
            
            while exists == False:
                for student in students:
                    account = student._account
                    if username.upper() == account.username.upper() and password == account.password:
                        print()
                        print('************************************************************')
                        print('Welcome to CICCC College!')
                        print('************************************************************')
                        input('Press enter to continue...')
                        exists = True
                        self.startPpalMenu(student)                                                                    
            
                print()
                print('************************************************************')
                print('Your account does not exist. Please try again!')
                print('************************************************************')
                print()
                username = input("enter the username: ")
                if username.upper() == "REGISTER":                        
                    student = self.register()       
                    exists = True
                    self.startPpalMenu(student)
                else:
                    password = input("enter the password: ")         
    
        
def main():
    portalManager = PortalManager() #The portal manager gets created here
    portalManager.createATestPortal()  #The studends and courses get created here
    portalManager._createAllMenus()  #The menus get created here
    user = portalManager.login() #The program displays the login and ask the user to enter o register

main()
