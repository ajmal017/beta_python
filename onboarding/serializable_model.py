from django.db import models
from onboarding.serializer import  Serialize


class SerializableModelCustom(models.Model):
    def __str__(self):
        pass

class SerializableModelNodes(models.Model):
    def __str__(self):
        return "<"+self.__class__.__name__+">"+Serialize(self, False)+"</"+self.__class__.__name__+">"
    def __str__(self,node_name):
        return "<"+node_name+">"+Serialize(self, False)+"</"+node_name+">"

class SerializableModelInline(models.Model):
    def __str__(self):
        return "<"+self.__class__.__name__+Serialize(self, True)+"/>"
    def __str__(self, node_name):
        return "<"+node_name+Serialize(self, True)+"/>"