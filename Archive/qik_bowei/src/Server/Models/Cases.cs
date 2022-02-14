using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

namespace backend.Models{
    public class Cases{
        [BsonId]
        [BsonRepresentation(BsonType.ObjectId)]
        public ObjectId _id { get; set; }
        public string CaseID {get;set;}
        public string CaseName {get;set;}
        public string CaseDesc {get;set;}
        public string CrimeType {get;set;}
        public string Comments {get;set;}
        public string Status {get;set;}
        public string Creator {get;set;}
        public string[] Assignee {get;set;}
        public string Priority {get;set;}
        public BsonDocument CreateTime {get;set;}
        public BsonDocument CloseTime {get;set;}
        public string CloseBy {get;set;}
        public BsonArray Evidences {get;set;}
        public string[] Jobs {get;set;}
        public string CyvestigoCaseId {get;set;}

        public Cases()
        {
            _id = ObjectId.GenerateNewId();
        }

    }
}


