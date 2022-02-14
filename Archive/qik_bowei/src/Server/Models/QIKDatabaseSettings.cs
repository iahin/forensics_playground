namespace backend.Models
{
    public class QIKDatabaseSettings : IQIKDatabaseSettings
    {
        public string QIKRepositoryCollectionName { get;set; }
        public string CasesCollectionName { get;set; }
        public string ChainOfCustodyCollectionName { get;set; }
        public string UsersCollectionName { get;set; }
        public string ConnectionString { get; set; }
        public string DatabaseName { get; set; }
    }

    public interface IQIKDatabaseSettings
    {
        string QIKRepositoryCollectionName { get;set; }
        string CasesCollectionName { get;set; }
        string ChainOfCustodyCollectionName { get;set; }
        string UsersCollectionName { get;set; }
        string ConnectionString { get; set; }
        string DatabaseName { get; set; }
    }
}