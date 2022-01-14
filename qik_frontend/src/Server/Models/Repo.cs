using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

namespace backend.Models{
    public class Repo{
        [BsonId]
        [BsonRepresentation(BsonType.ObjectId)]
        public ObjectId _id { get; set; }
        public string Description { get; set; }
        public string CrimeType { get; set; }
        public string Investigator { get; set; }
        public string Query { get; set; }
        public string Repository { get; set; }
        public string Status { get; set; }
        public string DateTimeCreated { get; set; }
        public string QueryBuilder { get; set; }
        public string NodesData { get; set; }
        public string Title { get; set; }
        public Repo()
        {
            _id = ObjectId.GenerateNewId();
        }
    }
}