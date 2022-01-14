using backend.Models;
using backend.Services;
using Microsoft.AspNetCore.Mvc;
using System.Collections.Generic;
using MongoDB.Bson;

namespace backend.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class RepoController : ControllerBase
    {
        private readonly RepoService _qikService;

        public RepoController(RepoService qikService)
        {
            _qikService = qikService;
        }

        [HttpGet]
        public ActionResult<List<dynamic>> Get() =>
            _qikService.Get();

        [HttpGet("RetrieveOne")]
        public ActionResult<Repo> RetrieveOne(string id) =>
            _qikService.RetrieveOne(id);

        [HttpPost("Create")]
        public string Create(Repo repo)
        {
            _qikService.Create(repo);
            return repo._id + " had been successfully created";
        }

        [HttpPost("Update")]
        public string Update(string id, Repo repo){
            repo._id = ObjectId.Parse(id);
            _qikService.Update(repo);
            return repo._id + " had been successfully updated";
        }
    }
}