using backend.Models;
using MongoDB.Driver;
using System.Collections.Generic;
using System.Linq;

namespace backend.Services
{
    public class CasesService
    {
        private readonly IMongoCollection<dynamic> _cases;
        private readonly IMongoCollection<Cases> _casesType;

        public CasesService(IQIKDatabaseSettings settings)
        {
            var client = new MongoClient(settings.ConnectionString);
            var database = client.GetDatabase(settings.DatabaseName);
            _cases = database.GetCollection<dynamic>(settings.CasesCollectionName);
            _casesType = database.GetCollection<Cases>(settings.CasesCollectionName);
        }

        public List<dynamic> Get() =>
            _cases.Find(Cases => true).ToList();        

        public dynamic Create(dynamic cases)
        {
            _cases.InsertOne(cases);
            return cases;
        }
        public List<Cases> SearchAllCases(string parameter){
            List<Cases> CaseID = SearchCaseID(parameter);    
            List<Cases> CaseName = SearchCaseName(parameter);
            List<Cases> CaseDesc = SearchCaseDescription(parameter);
            List<Cases> CaseType = SearchCaseType(parameter);
            List<Cases> CaseStatus = SearchCaseStatus(parameter);
            List<Cases> CaseCreator = SearchCaseCreator(parameter);
            List<Cases> CaseAssignee = SearchCaseAssignee(parameter);
            List<Cases> CasePriority = SearchCasePriority(parameter);    
            return CaseID.Concat(CaseName).Concat(CaseDesc).Concat(CaseType).Concat(CaseStatus).Concat(CaseCreator).Concat(CaseAssignee).Concat(CasePriority).ToList();
        }
        public List<Cases> SearchCaseID(string parameter){
            return _casesType.Find(x => x.CaseID == parameter).ToList();
        }
        public List<Cases> SearchCaseName(string parameter){
            return _casesType.Find(x => x.CaseName == parameter).ToList();
        }
        public List<Cases> SearchCaseDescription(string parameter){
            return _casesType.Find(x => x.CaseDesc == parameter).ToList();
        }
        public List<Cases> SearchCaseType(string parameter){
            return _casesType.Find(x => x.CrimeType == parameter).ToList();
        }
        public List<Cases> SearchCaseStatus(string parameter){
            return _casesType.Find(x => x.Status == parameter).ToList();
        }
        public List<Cases> SearchCaseCreator(string parameter){
            return _casesType.Find(x => x.Creator == parameter).ToList();
        }
        public List<Cases> SearchCaseAssignee(string parameter){
            return _casesType.Find(x => x.Assignee[0] == parameter).ToList();
        }
        public List<Cases> SearchCasePriority(string parameter){
            return _casesType.Find(x => x.Priority == parameter).ToList();
        }
    }
}