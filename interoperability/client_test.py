"""
*******************************************************************
  Copyright (c) 2013, 2017 IBM Corp.

  All rights reserved. This program and the accompanying materials
  are made available under the terms of the Eclipse Public License v1.0
  and Eclipse Distribution License v1.0 which accompany this distribution.

  The Eclipse Public License is available at
     http://www.eclipse.org/legal/epl-v10.html
  and the Eclipse Distribution License is available at
    http://www.eclipse.org/org/documents/edl-v10.php.

  Contributors:
     Ian Craggs - initial implementation and/or documentation
*******************************************************************
"""

import unittest

import mqtt.clients.V311 as mqtt_client, time, logging, socket, sys, getopt, traceback

class Callbacks(mqtt_client.Callback):

  def __init__(self):
    self.messages = []
    self.publisheds = []
    self.subscribeds = []
    self.unsubscribeds = []

  def clear(self):
    self.__init__()

  def connectionLost(self, cause):
    logging.info("connectionLost %s", str(cause))

  def publishArrived(self, topicName, payload, qos, retained, msgid):
    logging.info("publishArrived %s %s %d %d %d", topicName, payload, qos, retained, msgid)
    self.messages.append((topicName, payload, qos, retained, msgid))
    return True

  def published(self, msgid):
    logging.info("published %d", msgid)
    self.publisheds.append(msgid)

  def subscribed(self, msgid, data):
    logging.info("subscribed %d", msgid)
    self.subscribeds.append((msgid, data))

  def unsubscribed(self, msgid):
    logging.info("unsubscribed %d", msgid)
    self.unsubscribeds.append(msgid)

def cleanup():
    # clean all client state
    print("clean up starting")
    print(clientid1,clientid2)
    clientids = (clientid1, clientid2)
    
    for clientid in clientids:
        curclient = mqtt_client.Client(clientid.encode("utf-8"))
        curclient.connect(host=host, port=port, cleansession=True)
        time.sleep(.1)
        curclient.disconnect()
        time.sleep(.1)

    # clean retained messages
    callback = Callbacks()
    curclient = mqtt_client.Client("clean retained".encode("utf-8"))
    curclient.registerCallback(callback)
    curclient.connect(host=host, port=port, cleansession=True)
    curclient.subscribe(["#"], [0])
    time.sleep(2) # wait for all retained messages to arrive
    for message in callback.messages:
        if message[3]: # retained flag
            print("deleting retained message for topic", message[0])
            curclient.publish(message[0], b"", 0, retained=True)
    curclient.disconnect()
    time.sleep(.1)
    print("clean up finished")
    
    
def topictest(self,sub_index=None,pub_index=None,message=None):
    #不同种类的topic测试
    callback.clear()
    callback2.clear()
    #用户B连接
    bclient.connect(host=host, port=port, cleansession=True)
    bclient.subscribe([wildtopics[sub_index]], [2])
    time.sleep(1) # wait for all retained messages, hopefully
#     callback2.clear()
    bclient.publish(topics[pub_index], message, 1, retained=False)
    time.sleep(2)
    #用户a连接
    aclient.connect(host=host, port=port, cleansession=True)
    aclient.publish(topics[pub_index], message, 1, retained=False)
    time.sleep(1)
    aclient.disconnect()
    time.sleep(1)
    bclient.disconnect()
    print(callback2.messages)
    return callback2.messages

def qostest(self,sub_qos=None,pub_qos=None,message=None):
    callback.clear()
    callback2.clear()
    #用户B连接
    bclient.connect(host=host, port=port, cleansession=True)
    bclient.subscribe([wildtopics[6]], [sub_qos])
    time.sleep(1) # wait for all retained messages, hopefully
#     callback2.clear()
    bclient.publish(topics[1], message, pub_qos, retained=False)
    time.sleep(2)
    #用户a连接
    aclient.connect(host=host, port=port, cleansession=True)
    aclient.publish(topics[1], message, pub_qos, retained=False)
    time.sleep(1)
    bclient.disconnect()
    time.sleep(1)
    aclient.disconnect()
    print(callback2.messages)
    return callback2.messages
def will_message_qos(self,willQos=None,subQos=None):
    succeeded = True
    callback2.clear()
    assert len(callback2.messages) == 0, callback2.messages
    connack = aclient.connect(host=host, port=port, cleansession=True, willFlag=True,
      willTopic=topics[2], willMessage=b"test will message qos zero", keepalive=2,willQoS=willQos)
    assert connack.flags == 0x00 # Session present
    connack = bclient.connect(host=host, port=port, cleansession=False)
    bclient.subscribe([topics[2]], [subQos])
    time.sleep(.1)
    aclient.terminate()
    time.sleep(5)
    bclient.disconnect()
    print(callback2.messages)
    return callback2.messages


def test_will_message_qos_zero(self):
      # will messages
      print("Will message test starting")
      succeeded = True
      callback2.clear()
      assert len(callback2.messages) == 0, callback2.messages
      try:
        connack = aclient.connect(host=host, port=port, cleansession=True, willFlag=True,
          willTopic=topics[2], willMessage=b"client not disconnected", keepalive=2,willQoS=0)
        assert connack.flags == 0x00 # Session present
        connack = bclient.connect(host=host, port=port, cleansession=False)
        bclient.subscribe([topics[2]], [0])
        time.sleep(.1)
        aclient.terminate()
        time.sleep(5)
        bclient.disconnect()
        print(callback2.messages)
        assert len(callback2.messages) == 1, callback2.messages  # should have the will message
        self.assertEqual(callback2.messages[0][1],b"client not disconnected")
      except:
        traceback.print_exc()
        succeeded = False
      print("Will message test", "succeeded" if succeeded else "failed")
      self.assertEqual(succeeded, True)
      return succeeded


def clientidtest(self,clientid,username,password):
    print("clientid test starting")
    succeeded = True
    try:
        client0 = mqtt_client.Client(clientid.encode("utf-8"))
        fails = True
        try:
            client0.connect(host=host, port=port, cleansession=False,username=username,password=password) # should work
        except:
            fails = False
        self.assertEqual(fails, True)
        fails = True
        try:
            client0.connect(host=host, port=port, cleansession=True,username=username,password=password) # should work
        except:
            fails = False
        self.assertEqual(fails, True)
        client0.disconnect()
    except:
        traceback.print_exc()
        succeeded = False
    print("error appkey clientid test", "succeeded" if succeeded else "failed")
    self.assertEqual(succeeded, True)
    return succeeded    
def usage():
  print(
"""
 -h: --hostname= hostname or ip address of server to run tests against
 -p: --port= port number of server to run tests against
 -z: --zero_length_clientid run zero length clientid test
 -d: --dollar_topics run $ topics test
 -s: --subscribe_failure run subscribe failure test
 -n: --nosubscribe_topic_filter= topic filter name for which subscriptions aren't allowed

""")

class Test(unittest.TestCase):
    global topics, wildtopics, nosubscribe_topics,host,port,clientid1,clientid2,authentication,username,orgpassword,apppassword,error_cliendid
    authentication = True
    username = "mqtttest"
    orgpassword = "$t$YWMt0XYa3p3FEeuJ29MjuiXwsgAAAAAAAAAAAAAAAAAAAAFDtjwasNNKD6W3CET2O3RNAQMAAAF41K2eOgBPGgB7wnftLV7vUoduVpU8pQF9135qUFD1UO2l2HQ57OkB3g"
    apppassword = "$t$YWMtr2pv5J3FEeuy4xGo09qdoQAAAAAAAAAAAAAAAAAAAAHywVI9t0RIZr9nfTCWbJvFAgMAAAF41Ky_GwBPGgDy9gnYcIUcK3qfB_HAXZ4TUC8FxCM1GesUxiXocoHnWA"
    topics =  ("TopicA", "TopicA/B", "Topic/C", "TopicA/C", "/TopicA","TopicA/B/C")
    clientid1 = "myclientid"  #开启鉴权后clientid格式为username@appkey 例如：shuang1@easemob-demo#chatdemoui
    clientid2 = "myclientid2"
    appkey = "easemob-demo#chatdmeoui"
    no_appkey = ""
    error_appkey = ""
    error_cliendid = {"error_appkey":"shuang2@"+error_appkey,"no_key":"shuang2@" + no_appkey,"correct_appkey_name":"shuang110@"+appkey}
    wildtopics = ("TopicA/+", "+/C", "#", "/#", "/+", "+/+", "TopicA/#","+/#")
    nosubscribe_topics = ("test/nosubscribe",)
    host = "47.99.177.19"
    port = 1883
    
    @classmethod
    def setUpClass(cls):
      global callback, callback2, aclient, bclient
      cleanup()

      callback = Callbacks()
      callback2 = Callbacks()

      #aclient = mqtt_client.Client(b"\xEF\xBB\xBF" + "myclientid".encode("utf-8"))
      aclient = mqtt_client.Client(clientid1.encode("utf-8"))
      aclient.registerCallback(callback)

      bclient = mqtt_client.Client(clientid2.encode("utf-8"))
      bclient.registerCallback(callback2)
    
    def setUp(self):
        callback.clear()
        callback2.clear()
    
    def tearDown(self):
        cleanup()

    def testBasic(self):
      print("Basic test starting")
      global aclient
      succeeded = True
      try:
        aclient.connect(host=host, port=port)
        aclient.disconnect()

        connack = aclient.connect(host=host, port=port)
        assert connack.flags == 0x00 # Session present
        aclient.subscribe([topics[0]], [2])
        aclient.publish(topics[0], b"qos 0")
        aclient.publish(topics[0], b"qos 1", 1)
        aclient.publish(topics[0], b"qos 2", 2)
        time.sleep(2)
        aclient.disconnect()
        print(callback.messages)
        self.assertEqual(len(callback.messages), 3)
      except:
        traceback.print_exc()
        succeeded = False
        
      print("Basic test", "succeeded" if succeeded else "failed")
      self.assertEqual(succeeded, True)
      return succeeded
    
    def test_cleansession_false(self):
      print("cleansession false test starting")
      global aclient
      succeeded = True
      try:
        callback.clear()
        connack = aclient.connect(host=host, port=port,cleansession=False)
        assert connack.flags == 0x00 # Session present
        aclient.subscribe([topics[0]], [2])
        aclient.disconnect()
        time.sleep(2)
        connack = aclient.connect(host=host, port=port,cleansession=False)
        time.sleep(2)
        connack1 = bclient.connect(host=host, port=port,cleansession=True)
        bclient.publish(topics[0], b"qos1", 1, retained=False)
        aclient.disconnect()
        print(callback.messages)
        self.assertEqual(len(callback.messages), 1)
        self.assertEqual(callback.messages[0][1], b"qos1")
      except:
        traceback.print_exc()
        succeeded = False
        
      print("Cleansession false test", "succeeded" if succeeded else "failed")
      self.assertEqual(succeeded, True)
      return succeeded
    
    
    #测试服务质量为零
    def test_qos_zero(self):
        print("QoS is minimized test starting")
        message = b"QoS is minimized "
        sub_qos = 0
        result = []
        succeeded = True
        try:
            result = qostest(self,sub_qos=sub_qos,pub_qos=0,message=message)
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0][2],sub_qos,result[0][2])
            self.assertEqual(result[1][2],sub_qos,result[0][2])
        except:
            succeeded = False
        self.assertTrue(succeeded)
        try:
            result1 = qostest(self,sub_qos=0,pub_qos=1,message=message)
            self.assertEqual(len(result1), 2)
            self.assertEqual(result1[0][2],sub_qos,result1[0][2])
            self.assertEqual(result1[1][2],sub_qos,result1[0][2])
        except:
            succeeded = False
        self.assertTrue(succeeded)
        try:
            result2 = qostest(self,sub_qos=0,pub_qos=2,message=message)
            self.assertEqual(len(result2), 2)
            self.assertEqual(result2[0][2],sub_qos,result2[0][2])
            self.assertEqual(result2[1][2],sub_qos,result2[0][2])
        except:
            succeeded = False
        print("QoS minimum test was ","succeeded" if succeeded else "falsed")
        self.assertTrue(succeeded)
    
    #测试服务质量为1
    def test_qos_one(self):
        print("QoS is minimized test starting")
        message = b"QoS is minimized "
        sub_qos = 1
        result = []
        succeeded = True
        try:
            result = qostest(self,sub_qos=sub_qos,pub_qos=0,message=message)
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0][2],0,result[0][2])
            self.assertEqual(result[1][2],0,result[0][2])
        except:
            succeeded = False
        self.assertTrue(succeeded)
        try:
            result1 = qostest(self,sub_qos=sub_qos,pub_qos=1,message=message)
            self.assertEqual(len(result1), 2)
            self.assertEqual(result1[0][2],sub_qos,result1[0][2])
            self.assertEqual(result1[1][2],sub_qos,result1[0][2])
        except:
            succeeded = False
        self.assertTrue(succeeded)
        try:
            result2 = qostest(self,sub_qos=sub_qos,pub_qos=2,message=message)
            self.assertEqual(len(result2), 2)
            self.assertEqual(result2[0][2],sub_qos,result2[0][2])
            self.assertEqual(result2[1][2],sub_qos,result2[0][2])
        except:
            succeeded = False
        print("QoS minimum test was ","succeeded" if succeeded else "falsed")
        self.assertTrue(succeeded)
            
    #测试服务质量为2
    def test_qos_two(self):
        print("QoS is minimized test starting")
        message = b"QoS is minimized "
        sub_qos = 2
        result = []
        succeeded = True
        try:
            result = qostest(self,sub_qos=sub_qos,pub_qos=0,message=message)
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0][2],0,result[0][2])
            self.assertEqual(result[1][2],0,result[0][2])
        except:
            succeeded = False
        self.assertTrue(succeeded)
        try:
            result1 = qostest(self,sub_qos=sub_qos,pub_qos=1,message=message)
            self.assertEqual(len(result1), 2)
            self.assertEqual(result1[0][2],1,result1[0][2])
            self.assertEqual(result1[1][2],1,result1[0][2])
        except:
            succeeded = False
        self.assertTrue(succeeded)
        try:
            result2 = qostest(self,sub_qos=sub_qos,pub_qos=2,message=message)
            self.assertEqual(len(result2), 2)
            self.assertEqual(result2[0][2],2,result2[0][2])
            self.assertEqual(result2[1][2],2,result2[0][2])
        except:
            succeeded = False
        print("QoS minimum test was ","succeeded" if succeeded else "falsed")
        self.assertTrue(succeeded)        
        

    def test_newsocket_false(self):
        print("the test newcocket is false starting")
        succeeded = True
        try:
            aclient.connect(host=host, port=port)
            aclient.connect(host=host, port=port, newsocket=False) # should fail - second connect on socket
            succeeded = False
        except Exception as exc:
            pass # exception expected
        print("the newcocket test","succeeded" if succeeded else "failed")
        self.assertTrue(succeeded)

    def test_wrong_protocol_name(self):
        print("the test wrong protocol name starting")
        succeeded = True
        try:
            aclient.connect(host=host, port=port, protocolName="hj") # should fail - wrong protocol name
            succeeded = False
        except Exception as exc:
            pass # exception expected
        print("Wrong protocol name test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded

    def test_retained_messages(self):
#         qos0topic="fromb/qos 0"
#         qos1topic="fromb/qos 1"
#         qos2topic="fromb/qos2"
#         wildcardtopic="fromb/+"
        print("Retained message test starting")
        succeeded = False
        try:
            # retained messages
            callback.clear()
            connack = aclient.connect(host=host, port=port, cleansession=True)
            assert connack.flags == 0x00 # Session present
            aclient.publish(topics[1], b"qos 0", 0, retained=True)
            aclient.publish(topics[2], b"qos 1", 1, retained=True)
            aclient.publish(topics[3], b"qos 2", 2, retained=True)
            time.sleep(1)
            aclient.subscribe([wildtopics[5]], [2])
            time.sleep(1)
            aclient.disconnect()
            print(callback.messages)
            print(callback.messages[0][1])
            assert len(callback.messages) == 3
            #目前排序是按照topic命名排序
            self.assertEqual(callback.messages[0][1],b"qos 1")
            self.assertEqual(callback.messages[1][1],b"qos 0")
            self.assertEqual(callback.messages[2][1],b"qos 2")

            # clear retained messages
            callback.clear()
            connack = aclient.connect(host=host, port=port, cleansession=True)
            assert connack.flags == 0x00 # Session present
            aclient.publish(topics[1], b"", 0, retained=True)
            aclient.publish(topics[2], b"", 1, retained=True)
            aclient.publish(topics[3], b"", 2, retained=True)
            time.sleep(1) # wait for QoS 2 exchange to be completed
            aclient.subscribe([wildtopics[5]], [2])
            time.sleep(1)
            aclient.disconnect()

            assert len(callback.messages) == 0, "callback messages is %s" % callback.messages
            succeeded = True
        except:
            traceback.print_exc()
        print("Retained message test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded
    
    
    def test_nosub_reatin_message(self):
        print("nosub reatin message test starting")
        succeeded = False
        try:
            # retained messages
            callback.clear()
            callback2.clear()
            connack = aclient.connect(host=host, port=port, cleansession=True)
            assert connack.flags == 0x00 # Session present
            aclient.publish(topics[1], b"qos 0", 0, retained=True)
#             aclient.publish(topics[2], b"qos 1", 1, retained=True)
            aclient.publish(topics[1], b"qos 1", 1, retained=True)
            aclient.publish(topics[1], b"qos 2", 2, retained=True)
            time.sleep(1)
#             aclient.disconnect()
#             time.sleep(1)
            connack = bclient.connect(host=host, port=port, cleansession=True)
            bclient.subscribe([topics[1]], [2])
            time.sleep(1)
            print(callback2.messages)
            assert len(callback2.messages) == 1
            self.assertEqual(callback2.messages[0][1], b"qos 2")
            succeeded = True
        except:
            traceback.print_exc()
        print("nosub reatin message test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded
    
    
    def test_reatin_true_false_message(self):
        print("reatin is true and false message test starting")
        succeeded = False
        try:
            # retained messages
            callback.clear()
            callback2.clear()
            connack = bclient.connect(host=host, port=port, cleansession=True)
            bclient.subscribe([topics[1]], [2])
            
            connack = aclient.connect(host=host, port=port, cleansession=True)
            assert connack.flags == 0x00 # Session present
            aclient.publish(topics[1], b"qos 0", 0, retained=True)
#             aclient.publish(topics[2], b"qos 1", 1, retained=True)
            aclient.publish(topics[1], b"qos 1", 1, retained=False)
            aclient.publish(topics[1], b"qos 2", 2, retained=True)
#             aclient.publish(topics[1], b"", 2, retained=True)
            time.sleep(1)
            aclient.disconnect()
            time.sleep(1)
            bclient.disconnect()
            print(callback2.messages)
            print(len(callback2.messages))
            assert len(callback2.messages) == 3
            self.assertEqual(callback2.messages[0][1], b"qos 0")
            self.assertEqual(callback2.messages[1][1], b"qos 1")
            self.assertEqual(callback2.messages[2][1], b"qos 2")
            succeeded = True
        except:
            traceback.print_exc()
        print("reatin is true and false message test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded
    
    def test_will_message(self):
      # will messages
      print("Will message test starting")
      succeeded = True
      callback2.clear()
      assert len(callback2.messages) == 0, callback2.messages
      try:
        connack = aclient.connect(host=host, port=port, cleansession=True, willFlag=True,
          willTopic=topics[2], willMessage=b"client not disconnected", keepalive=2)
        assert connack.flags == 0x00 # Session present
        connack = bclient.connect(host=host, port=port, cleansession=False)
        bclient.subscribe([topics[2]], [2])
        time.sleep(.1)
        aclient.terminate()
        time.sleep(5)
        bclient.disconnect()
        print(callback2.messages)
        assert len(callback2.messages) == 1, callback2.messages  # should have the will message
        self.assertEqual(callback2.messages[0][1],b"client not disconnected")
      except:
        traceback.print_exc()
        succeeded = False
      print("Will message test", "succeeded" if succeeded else "failed")
      self.assertEqual(succeeded, True)
      return succeeded
  
    #未订阅遗嘱topic不会收到消息
    def test_nosub_will_message(self):
        print("nosub will message test starting")
        succeeded = True
        callback2.clear()
        assert len(callback2.messages) == 0, callback2.messages
        try:
            connack = aclient.connect(host=host, port=port, cleansession=True, willFlag=True,
              willTopic=topics[2], willMessage=b"client not disconnected", keepalive=2)
            assert connack.flags == 0x00 # Session present
            connack = bclient.connect(host=host, port=port, cleansession=False)
            bclient.subscribe([topics[3]], [2])
            time.sleep(.1)
            aclient.terminate()
            time.sleep(5)
            bclient.disconnect()
            print(callback2.messages)
            assert len(callback2.messages) == 0, callback2.messages  # should have the will message
#             self.assertEqual(callback2.messages[0][1],b"client not disconnected")
        except:
            traceback.print_exc()
            succeeded = False
        print("nosub will message test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded
  
    #修改遗嘱消息
    def test_revise_will_message(self):
        print("revise will message test starting")
        print("test case is error")
        succeeded = True
        callback2.clear()
        assert len(callback2.messages) == 0, callback2.messages
        try:
            connack = aclient.connect(host=host, port=port, cleansession=False, willFlag=True,
              willTopic=topics[2], willMessage=b"client not disconnected", keepalive=2)
            assert connack.flags == 0x00 # Session present
            connack = bclient.connect(host=host, port=port, cleansession=False)
            bclient.subscribe([topics[2]], [2])
            time.sleep(1)
            print("the fist will message is %s"%(callback2.messages))
            time.sleep(.1)
            connack = aclient.connect(host=host, port=port, cleansession=True,newsocket=False,willFlag=True,
              willTopic=topics[2], willMessage=b"client not disconnected", keepalive=2)
            aclient.terminate()
            time.sleep(5)
            bclient.disconnect()
            print(callback2.messages)
            assert len(callback2.messages) == 1, callback2.messages  # should have the will message
            self.assertEqual(callback2.messages[0][1],b"revise will menssage")
        except:
            traceback.print_exc()
            succeeded = False
        print("revise will message test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded
    
    #测试遗嘱消息服务质量为零与订阅此topic，服务质量取最小值
    def test_will_message_qos_zero(self):
        # will messages
        print("Will message qos0 test starting")
        willQos=0
        succeeded = True
        try:
            result = will_message_qos(self,willQos=willQos,subQos=0)
            assert len(result) == 1
            self.assertEqual(result[0][2],0)
        except:
            traceback.print_exc()
            succeeded = False
        try:
            result = will_message_qos(self,willQos=willQos,subQos=1)
            assert len(result) == 1
            self.assertEqual(result[0][2],0)
        except:
            traceback.print_exc()
            succeeded = False
        try:
            result = will_message_qos(self,willQos=willQos,subQos=2)
            assert len(result) == 1
            self.assertEqual(result[0][2],0)
        except:
            traceback.print_exc()
            succeeded = False
        print("Will message qos0 test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        
    #测试遗嘱消息服务质量为1与订阅此topic，服务质量取最小值
    def test_will_message_qos_one(self):
        print("Will message qos1 test starting")
        willQos=1
        succeeded = True
        try:
            result = will_message_qos(self,willQos=willQos,subQos=0)
            assert len(result) == 1
            self.assertEqual(result[0][2],0)
        except:
            traceback.print_exc()
            succeeded = False
        try:
            result = will_message_qos(self,willQos=willQos,subQos=1)
            assert len(result) == 1
            self.assertEqual(result[0][2],willQos)
        except:
            traceback.print_exc()
            succeeded = False
        try:
            result = will_message_qos(self,willQos=willQos,subQos=2)
            assert len(result) == 1
            self.assertEqual(result[0][2],willQos)
        except:
            traceback.print_exc()
            succeeded = False
        print("Will message qos1 test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
    
    
        #测试遗嘱消息服务质量为2与订阅此topic，服务质量取最小值
    def test_will_message_qos_two(self):
        # will messages
        print("Will message qos2 test starting")
        willQos=2
        succeeded = True
        try:
            result = will_message_qos(self,willQos=willQos,subQos=0)
            assert len(result) == 1
            self.assertEqual(result[0][2],0)
        except:
            traceback.print_exc()
            succeeded = False
        try:
            result = will_message_qos(self,willQos=willQos,subQos=1)
            assert len(result) == 1
            self.assertEqual(result[0][2],1)
        except:
            traceback.print_exc()
            succeeded = False
        try:
            result = will_message_qos(self,willQos=willQos,subQos=2)
            assert len(result) == 1
            self.assertEqual(result[0][2],willQos)
        except:
            traceback.print_exc()
            succeeded = False
        print("Will message qos2 test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return callback2.messages
  
    #clientid中存在错误的appkey
    @unittest.skipIf(authentication == True,"Not Run")
    def test_clientid_error_appkey(self):
        print("clientid_error_appkey test starting")
        clientid = error_cliendid["error_appkey"]
        print(clientid,username,orgpassword)
        succeeded = clientidtest(self,clientid,username,orgpassword)
        self.assertEqual(succeeded, True)
        print("clientid_error_appkey test starting")
        
        
    @unittest.skipIf(authentication == True,"Not Run")
    #clientid中使用不存在的appkey
    def test_no_appkey(self):
        print("clientid_no_appkey test starting")
        clientid = error_cliendid["no_appkey"]
        print(clientid,username,orgpassword)
        succeeded = clientidtest(self,clientid,username,apppassword)
        self.assertEqual(succeeded, True)
        print("clientid_no_appkey test starting")
        
        
    @unittest.skipIf(authentication == True,"Not Run")
    #client中使用正确的appkey，username
    def test_correct_appkey_name(self):
        print("clientid_no_appkey test starting")
        clientid = error_cliendid["correct_appkey_name"]
        print(clientid,username,orgpassword)
        succeeded = clientidtest(self,clientid,username,apppassword)
        self.assertEqual(succeeded, True)
        print("clientid_no_appkey test starting")
        
        
    # 0 length clientid
    def test_zero_length_clientid(self):
        print("Zero length clientid test starting")
        succeeded = True
        try:
            client0 = mqtt_client.Client("")
            fails = False
            try:
                client0.connect(host=host, port=port, cleansession=False) # should be rejected        
            except:
                fails = True
            print(fails)
            self.assertEqual(fails, True)
            fails = False
            try:
                client0.connect(host=host, port=port, cleansession=True) # should work
            except:
                fails = True
            self.assertEqual(fails, False)
            client0.disconnect()
        except:
            traceback.print_exc()
            succeeded = False
        print("Zero length clientid test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded,True)
        return succeeded

    def test_offline_message_queueing(self):
        succeeded = True
        try:
            # message queueing for offline clients
            callback.clear()
    
            connack = aclient.connect(host=host, port=port, cleansession=False)
            print(connack)
            print(connack.flags)
            aclient.subscribe([wildtopics[5]], [2])
            aclient.disconnect()
    
            connack = bclient.connect(host=host, port=port, cleansession=True)
            print(connack)
            print(connack.flags)
            assert connack.flags == 0x00 # Session present
            bclient.publish(topics[1], b"qos 0", 0)
            bclient.publish(topics[2], b"qos 1", 1)
            bclient.publish(topics[3], b"qos 2", 2)
            time.sleep(2)
            bclient.disconnect()
    
            connack = aclient.connect(host=host, port=port, cleansession=False)
            print(connack.flags)
            assert connack.flags == 0x01 # Session present
            time.sleep(2)
            aclient.disconnect()
            print(callback.messages)
            assert len(callback.messages) in [2, 3], callback.messages
            #目前排序是按照topic命名排序
            self.assertEqual(callback.messages[0][1],b"qos 1")
    #         self.assertEqual(callback.messages[1][1],b"qos 0")
            self.assertEqual(callback.messages[1][1],b"qos 2")
            print("This server %s queueing QoS 0 messages for offline clients" % \
                ("is" if len(callback.messages) == 3 else "is not"))
        except:
            traceback.print_exc()
            succeeded = False
        print("Offline message queueing test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded

    def test_overlapping_subscriptions(self):
      # overlapping subscriptions. When there is more than one matching subscription for the same client for a topic,
      # the server may send back one message with the highest QoS of any matching subscription, or one message for
      # each subscription with a matching QoS.
      print("Overlapping subscriptions test starting")
      succeeded = True
      try:
        callback.clear()
        callback2.clear()
        aclient.connect(host=host, port=port)
        #注释wildtopics[6]=="TopicA/#",wildtopics[0]="TopicA/+"
        aclient.subscribe([wildtopics[6], wildtopics[0]], [2, 1])
        #注释topics[3]="TopicA/C"
        aclient.publish(topics[3], b"overlapping topic filters", 2)
        time.sleep(1)
        print(callback.messages)
        assert len(callback.messages) in [1, 2]
        #打印出callback.messages
        if len(callback.messages) == 1:
          print("This server is publishing one message for all matching overlapping subscriptions, not one for each.")
          assert callback.messages[0][2] == 2
          self.assertCountEqual(callback.messages[0][1], b"overlapping topic filters")
        else:
          print("This server is publishing one message per each matching overlapping subscription.")
          assert (callback.messages[0][2] == 2 and callback.messages[1][2] == 1) or \
                 (callback.messages[0][2] == 1 and callback.messages[1][2] == 2), callback.messages
          self.assertCountEqual(callback.messages[0][1], b"overlapping topic filters")
          self.assertCountEqual(callback.messages[1][1], b"overlapping topic filters")
        aclient.disconnect()
      except:
        traceback.print_exc()
        succeeded = False
      print("Overlapping subscriptions test", "succeeded" if succeeded else "failed")
      self.assertEqual(succeeded, True)
      return succeeded


    def test_keepalive(self):
      # keep_alive processing.  We should be kicked off by the server if we don't send or receive any data, and don't send
      # any pings either.
      print("Keep_alive test starting")
      succeeded = True
      try:
        callback2.clear()
        aclient.connect(host=host, port=port, cleansession=True, keepalive=5, willFlag=True,
              willTopic=topics[4], willMessage=b'keepalive_expiry')
        bclient.connect(host=host, port=port, cleansession=True, keepalive=0)
        #注释topics[4]=TopicA/C
        bclient.subscribe([topics[4]], [2])
        time.sleep(15)
        bclient.disconnect()
        print(callback2.messages)
        self.assertEqual(callback2.messages[0][1], b"keepalive_expiry")
        assert len(callback2.messages) == 1, "length should be 1: %s" % callback2.messages # should have the will message
      except:
        traceback.print_exc()
        succeeded = False
      print("Keepalive test", "succeeded" if succeeded else "failed")
      self.assertEqual(succeeded, True)
      return succeeded


    def test_redelivery_on_reconnect(self):
      # redelivery on reconnect. When a QoS 1 or 2 exchange has not been completed, the server should retry the
      # appropriate MQTT packets
      print("Redelivery on reconnect test starting")
      succeeded = True
      try:
        callback.clear()
        callback2.clear()
        bclient.connect(host=host, port=port, cleansession=False)
        bclient.subscribe([wildtopics[6]], [2])
        bclient.pause() # stops responding to incoming publishes
        bclient.publish(topics[1], b"", 1, retained=False)  #注释topics[1]=TopicA/B,
        bclient.publish(topics[3], b"", 2, retained=False)  #注释topics[3]="TopicA/C"
        time.sleep(1)
        bclient.disconnect()
        assert len(callback2.messages) == 0, "length should be 0: %s" % callback2.messages
        bclient.resume()
        bclient.connect(host=host, port=port, cleansession=False)
        time.sleep(3)
        print(callback2.messages)
        assert len(callback2.messages) == 2
        self.assertEqual(callback2.messages[0][1], b"")
        self.assertEqual(callback2.messages[1][1], b"")
        bclient.disconnect()
      except:
        traceback.print_exc()
        succeeded = False
      print("Redelivery on reconnect test", "succeeded" if succeeded else "failed")
      self.assertEqual(succeeded, True)
      return succeeded

    def test_nosubscribe_end(self):
      # Subscribe failure.  A new feature of MQTT 3.1.1 is the ability to send back negative reponses to subscribe
      # requests.  One way of doing this is to subscribe to a topic which is not allowed to be subscribed to.
      #中文：此case主要验证了可以订阅/发布已nosubscribe结尾的topic
      print("nosubscribe end test starting")
      succeeded = True
      try:
        callback.clear()
        aclient.connect(host=host, port=port)
        aclient.subscribe([nosubscribe_topics[0]], [2])     #订阅已nosubscribe结尾的topic
        time.sleep(.2)
        # subscribeds is a list of (msgid, [qos])
        print(callback.subscribeds)
        #assert callback.subscribeds[0][1][0] == 0x80, "return code should be 0x80 %s" % callback.subscribeds
        self.assertCountEqual(callback.subscribeds[0][1], [2])
        #aclient.publish(wildtopics[0],b"Test the topic has nosubscribe end",2)
        aclient.publish(nosubscribe_topics[0], b"overlapping topic filters", 2)
        time.sleep(.2)
        assert len(callback.messages) == 1,"callback messages length is %d"%(len(callback.messages))
        
      except:
        traceback.print_exc()
        succeeded = False
      print("Nosubscribe end test", "succeeded" if succeeded else "failed")
      self.assertEqual(succeeded, True)
      return succeeded
    
    
    #验证topic通配符#
    def test_first_topic_format(self):
        print("topic/# topics test starting")
        succeeded = True
        message=b"test topic/#"
        callbackresult = []
        try:
            callbackresult = topictest(self,sub_index=6,pub_index=1, message=message)
            assert len(callbackresult) == 2
            self.assertEqual(callbackresult[0][1],message,callbackresult[0][1])
            self.assertEqual(callbackresult[1][1],message,callbackresult[0][1])
        except:
            traceback.print_exc()
            succeeded = False
        try:
            callbackresult = topictest(self,sub_index=6,pub_index=5, message=message)
            assert len(callbackresult) == 2
            self.assertEqual(callbackresult[0][1],message,callbackresult[0][1])
            self.assertEqual(callbackresult[1][1],message,callbackresult[0][1])
        except:
            traceback.print_exc()
            succeeded = False
        print(callbackresult)
        print("topic/# topics test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded
    
    
    #验证topic通配符+
    def test_second_topic_format(self):
        print("topics:topics/+ test starting")
        succeeded = True
        message=b"test topic:topic/#"
        callbackresult = []
        try:
            callbackresult = topictest(self,sub_index=0,pub_index=1,message=message)
            assert len(callbackresult) == 2,"callback length is %s"%(len(callback))
            self.assertEqual(callbackresult[0][1], message,callbackresult[0][1])
            self.assertEqual(callbackresult[1][1],message,callbackresult[0][1])
        except:
            traceback.print_exc()
            succeeded = False
        try:
            callbackresult = topictest(self,sub_index=0,pub_index=5,message=message)
#             self.assertEqual(callback[0][1], message,callback[0][1])
            assert len(callbackresult) == 0,print("层级不同无法接收到消息"+callbackresult)
        except:
            traceback.print_exc()
            succeeded = False
        print(callbackresult)
        print("topics:topics/+ test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded
    
    #验证topic通配符
    @unittest.skip("not run")
    def test_third_topic_format(self):
        print("topics format +/# test starting")
        succeeded = True
        message=b"test topic:+/#"
        callbackresult = []
        try:
            callbackresult = topictest(self,sub_index=0,pub_index=1,message=message)
            assert len(callbackresult) == 2,"callback length is %s"%(len(callback))
            self.assertEqual(callbackresult[0][1], message,callbackresult[0][1])
            self.assertEqual(callbackresult[1][1],message,callbackresult[0][1])
        except:
            traceback.print_exc()
            succeeded = False
        try:
            callbackresult = topictest(self,sub_index=0,pub_index=5,message=message)
            #self.assertEqual(callback[0][1], message,callback[0][1])
            assert len(callbackresult) == 0,print("层级不同无法接收到消息"+callbackresult)
        except:
            traceback.print_exc()
            succeeded = False
        print(callbackresult)
        print("topics format +/# test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded

    #验证topic通配符格式为+/#
    #@unittest.skip("由于目前使用EMQ的客户端测试，pub消息太多，导致卡死。目前不测试，需要修改case")
    def test_hourth_topic_format(self):
        print("topics format +/# test starting")   #由于目前使用EMQ的客户端测试，pub消息太多，导致卡死。目前不测试
        succeeded = True
        message=b"test topic:+/#"
        callbackresult = []
        try:
            callbackresult = topictest(self,sub_index=7,pub_index=1,message=message)
            self.assertEqual(len(callbackresult), 2,"callbackresult is %s"%(callbackresult))
            self.assertEqual(callbackresult[0][1],message)
            self.assertEqual(callbackresult[1][1],message)
        except:
            traceback.print_exc()
            succeeded = False
        try:
            callbackresult = topictest(self,sub_index=7,pub_index=5,message=message)
            self.assertEqual(len(callbackresult), 2,"callbackresult is $s"%(callbackresult))
            self.assertEqual(callbackresult[0][1],message)
            self.assertEqual(callbackresult[1][1],message)
        except:
            traceback.print_exc()
            succeeded = False
        print(callback)
        print("topics format +/#  test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded
    
    
    #验证topic格式为+/+匹配规则
    def test_fifth_topic_format(self):
        print("test topic:+/+ starting")
        succeeded = True
        try:
            callback.clear()
            connack = aclient.connect(host=host, port=port, cleansession=False)
            aclient.subscribe([wildtopics[5]], [2])
            connack = bclient.connect(host=host, port=port, cleansession=True)
            assert connack.flags == 0x00 # Session present
            bclient.publish(topics[1], b"qos 0", 0)
            bclient.publish(topics[2], b"qos 1", 1)
            bclient.publish(topics[3], b"qos 2", 2)
            time.sleep(1)
            print(callback.messages)
            assert len(callback.messages) == 3
            self.assertEqual(callback.messages[0][1],b"qos 0")
            self.assertEqual(callback.messages[1][1],b"qos 1")
            self.assertEqual(callback.messages[2][1],b"qos 2")
            
            time.sleep(2)
            aclient.disconnect()
            bclient.disconnect()
        except:
            traceback.print_exc()
            succeeded = False
        print("test topic:+/+ ", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded
  
  
    def test_dollar_topics(self):
        # $ topics. The specification says that a topic filter which starts with a wildcard does not match topic names that
        # begin with a $.  Publishing to a topic which starts with a $ may not be allowed on some servers (which is entirely valid),
        # so this test will not work and should be omitted in that case.
        #中文：此case主要验证了不能向已$开头的topic发布消息
        print("$ topics test starting")
        succeeded = True
        try:
            callback2.clear()
            bclient.connect(host=host, port=port, cleansession=True, keepalive=0)
            bclient.subscribe([wildtopics[5]], [2])
            time.sleep(1) # wait for all retained messages, hopefully
            callback2.clear()
            bclient.publish("$"+topics[1], b"", 1, retained=False)
            time.sleep(2)
            assert len(callback2.messages) == 0, callback2.messages
            bclient.disconnect()
        except:
            traceback.print_exc()
            succeeded = False
        print("$ topics test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded

    def test_unsubscribe(self):
        #中文：验证未订阅topic，不会收到此topic的消息
        print("Unsubscribe test starting")
        succeeded = True
        try:
            callback2.clear()
            bclient.connect(host=host, port=port, cleansession=True)
            bclient.subscribe([topics[0]], [2])
            bclient.subscribe([topics[1]], [2])
            bclient.subscribe([topics[2]], [2])
            time.sleep(1) # wait for all retained messages, hopefully
            # Unsubscribed from one topic
            bclient.unsubscribe([topics[0]])    #取消订阅topics[0]
    
            aclient.connect(host=host, port=port, cleansession=True)
            aclient.publish(topics[0], b"", 1, retained=False)
            aclient.publish(topics[1], b"", 1, retained=False)
            aclient.publish(topics[2], b"", 1, retained=False)
            time.sleep(2)
    
            bclient.disconnect()
            aclient.disconnect()
            print(callback2.messages)
            self.assertEqual(len(callback2.messages), 2, callback2.messages)
        except:
            traceback.print_exc()
            succeeded = False
        self.assertEqual(succeeded, True)
        print("unsubscribe tests", "succeeded" if succeeded else "failed")
        return 
    
    def test_repetition_sub(self):
        print("test repetition sub starting")
        succeeded = True
        try:
            callback2.clear()
            callback.clear()
            connack=bclient.connect(host=host, port=port)
            bclient.subscribe([topics[0]], [2])
            time.sleep(1)
            bclient.subscribe([topics[0]], [2])
            time.sleep(1) # wait for all retained messages, hopefully
            aclient.connect(host=host, port=port)
            aclient.publish(topics[0],b"test repetition sub starting", 1, retained=False)
            time.sleep(2)
            print(callback2.messages)
            self.assertEqual(len(callback2.messages), 1)
            self.assertEqual(callback2.messages[0][1], b"test repetition sub starting")
            bclient.disconnect()
        except:
            traceback.print_exc()
            succeeded = False
        self.assertEqual(succeeded, True)
        print("test repetition sub tests", "succeeded" if succeeded else "failed")
        return succeeded
    @unittest.skip("reason")
    def tset_1(self):
        print("Basic test starting")
        global aclient
        succeeded = True
        try:
            aclient.connect(host=host, port=port)
            aclient.disconnect()
    
            connack = aclient.connect(host=host, port=port)
            assert connack.flags == 0x00 # Session present
            aclient.subscribe([topics[0]], [2])
            aclient.publish(topics[0], b"qos 0")
            aclient.publish(topics[0], b"qos 1", 1)
            aclient.publish(topics[0], b"qos 2", 2)
            time.sleep(2)
            aclient.disconnect()
            print(callback.messages)
            self.assertEqual(len(callback.messages), 3)
        except:
            traceback.print_exc()
            succeeded = False
        
        print("Basic test", "succeeded" if succeeded else "failed")
        self.assertEqual(succeeded, True)
        return succeeded

if __name__ == "__main__":
    try:
      opts, args = getopt.gnu_getopt(sys.argv[1:], "h:p:zdsn:",
        ["help", "hostname=", "port=", "iterations="])
    except getopt.GetoptError as err:
      print(err) # will print something like "option -a not recognized"
      usage()
      sys.exit(2)

    iterations = 1
    for o, a in opts:
      if o in ("--help"):
        usage()
        sys.exit()
      elif o in ("-n", "--nosubscribe_topic_filter"):
        nosubscribe_topic_filter = a
      elif o in ("-h", "--hostname"):
        host = a
      elif o in ("-p", "--port"):
        port = int(a)
      elif o in ("--iterations"):
        iterations = int(a)
      else:
        assert False, "unhandled option"

    root = logging.getLogger()
    root.setLevel(logging.ERROR)

    print("hostname", host, "port", port)
 
    for i in range(iterations):
      unittest.main()
#     #创建测试集
#     suite = unittest.TestSuite()
#      #   suite.addTest(Test("testBasic"))
#     suite.addTest(Test("test_cleansession_false"))
# #     suite.addTest(Test("test_will_message_qos_one"))
# #     suite.addTest(Test("test_will_message_qos_two"))
# #     suite.addTest(Test("test_second_topic_format"))
# #     执行测试
#     runner = unittest.TextTestRunner(verbosity=2)
#     runner.run(suite)
