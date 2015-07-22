from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from database import Base
from datetime import datetime
from database import db_session

class LogEntry(Base):
    __tablename__ = 'log'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime(), default=datetime.utcnow)
    log_level_id = Column(Integer, default=1)
    text = Column(Text)

    @staticmethod
    def add(text, log_level_id=1):
        log_entry = LogEntry(text, log_level_id)
        db_session.add(log_entry)
        db_session.commit()
    
    def __init__(self, text=None, log_level_id=1):
        self.text = text
        self.log_level_id = log_level_id

    def __repr__(self):
        return '<LogEntry %r>' % (self.id)   
        
class PackageLogEntry(Base):
    __tablename__ = 'package_log'
    id = Column(Integer, primary_key=True)
    package = Column(String(50))
    timeout = Column(Integer)
    start_timestamp = Column(DateTime(), default=datetime.utcnow)
    end_timestamp = Column(DateTime())
    timed_out = Column(Boolean, default=False)
    errored = Column(Boolean, default=False)
    stdout = Column(Text)
    stderr = Column(Text)

    @staticmethod
    def start(package, timeout):
        package_log_entry = PackageLogEntry(package, timeout)
        db_session.add(package_log_entry)
        db_session.commit()   
        return package_log_entry
        
    @staticmethod
    def finish(package_log_entry):
        package_log_entry.end_timestamp = datetime.utcnow()
        db_session.add(package_log_entry)
        db_session.commit()        
    
    def __init__(self, package, timeout):
        self.package = package
        self.timeout = timeout

    def __repr__(self):
        return '<PackageLogEntry %r>' % (self.id)   
        