using backend.Models;
using MongoDB.Driver;
using System.Collections.Generic;
using System.Linq;
using MongoDB.Bson;
// using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace backend.Services
{
    public class RepoService
    {
        private readonly IMongoCollection<dynamic> _qik;
        private readonly IMongoCollection<Repo> _repo;

        public RepoService(IQIKDatabaseSettings settings)
        {
            var client = new MongoClient(settings.ConnectionString);
            var database = client.GetDatabase(settings.DatabaseName);
            _qik = database.GetCollection<dynamic>(settings.QIKRepositoryCollectionName);
            _repo = database.GetCollection<Repo>(settings.QIKRepositoryCollectionName);

            
        }

        public List<dynamic> Get() =>
            _qik.Find(Repo => true).ToList();

        //https://localhost:5001/api/repo/RetrieveOne?id=
        public Repo RetrieveOne(string id) =>
            _repo.Find<Repo>(Repo => Repo._id == ObjectId.Parse(id)).FirstOrDefault();

        public dynamic Create(dynamic Repo)
        {

            string qb = Repo.Query;
            var result = JObject.Parse(qb);
            var paramters = result["Query"];
            var elemMatch = paramters["$elemMatch"];
            string jsonresult = elemMatch.ToString(Newtonsoft.Json.Formatting.None);

            //trigger an api endpoint
            //receive response

            _qik.InsertOne(Repo);
            return Repo;
        }

        //https://localhost:5001/api/repo/Update?id=
        public void Update(Repo RepoIn) =>
            _repo.FindOneAndReplace(Repo => Repo._id == RepoIn._id, RepoIn);
    }
}